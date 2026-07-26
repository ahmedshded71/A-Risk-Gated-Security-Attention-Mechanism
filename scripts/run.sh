#!/bin/bash
set -e

# ==============================================================================
# Quick Run Script for RGSA-Transformer
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
${BLUE}RGSA-Transformer v5.6.2 - Docker helper${NC}

${YELLOW}Usage:${NC}
    $0 [command]

${YELLOW}Commands:${NC}
    build       Build the Docker image for CPU
    build-gpu   Build the Docker image for GPU
    run         Start the pipeline
    gpu         Start with GPU support
    shell       Open a shell inside the container
    logs        Follow the container logs
    stop        Stop the containers
    clean       Remove containers and images
    test        Run a quick verification

EOF
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
}

build_image() {
    log_info "Building Docker image (CPU)..."
    cd "$PROJECT_DIR"
    docker build -t rgsa-transformer:5.6.2-cpu -f Dockerfile .
    log_info "Build complete"
}

build_gpu_image() {
    log_info "Building Docker image (GPU)..."
    cd "$PROJECT_DIR"
    docker build -t rgsa-transformer:5.6.2-gpu -f Dockerfile.gpu .
    log_info "GPU build complete"
}

run_container() {
    log_info "Starting RGSA-Transformer..."
    
    mkdir -p "$PROJECT_DIR/outputs"
    
    if [ ! "$(ls -A $PROJECT_DIR/data 2>/dev/null | grep -v '.gitkeep')" ]; then
        log_warn "No datasets found in data/ directory"
        log_warn "Please place your CSV files in: $PROJECT_DIR/data/"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    cd "$PROJECT_DIR"
    docker compose up --build
}

run_gpu_container() {
    log_info "Starting RGSA-Transformer with GPU..."
    
    if ! command -v nvidia-smi &> /dev/null; then
        log_error "nvidia-smi not found. GPU support requires NVIDIA drivers."
        exit 1
    fi
    
    mkdir -p "$PROJECT_DIR/outputs"
    cd "$PROJECT_DIR"
    docker compose -f docker-compose.gpu.yml up --build
}

open_shell() {
    log_info "Opening shell in container..."
    cd "$PROJECT_DIR"
    docker compose run --rm rgsa-transformer bash
}

view_logs() {
    cd "$PROJECT_DIR"
    docker compose logs -f rgsa-transformer
}

stop_container() {
    log_info "Stopping containers..."
    cd "$PROJECT_DIR"
    docker compose down
}

clean_all() {
    log_warn "This will remove all containers and images"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd "$PROJECT_DIR"
        docker compose down -v --rmi all
        docker system prune -f
        log_info "Cleanup complete"
    fi
}

run_test() {
    log_info "Running quick test..."
    cd "$PROJECT_DIR"
    docker compose run --rm rgsa-transformer python -c "
import rgsa
print(f'RGSA-Transformer v{rgsa.__version__} loaded successfully')
from rgsa.models import build_rgsa_base
model = build_rgsa_base(input_dim=78)
print(f'Model built: {model.count_params():,} parameters')
"
}

# Main
check_prerequisites

case "${1:-}" in
    build)
        build_image
        ;;
    build-gpu)
        build_gpu_image
        ;;
    run)
        run_container
        ;;
    gpu)
        run_gpu_container
        ;;
    shell)
        open_shell
        ;;
    logs)
        view_logs
        ;;
    stop)
        stop_container
        ;;
    clean)
        clean_all
        ;;
    test)
        run_test
        ;;
    --help|-h|help)
        usage
        ;;
    *)
        log_error "Unknown command: ${1:-}"
        usage
        exit 1
        ;;
esac
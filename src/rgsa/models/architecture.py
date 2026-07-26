"""RGSA-Transformer architecture: Security Tokenizer + Risk-Gated Attention."""
import tensorflow as tf
from tensorflow.keras import layers, Model
from rgsa.config import HYPERPARAMS


class SecurityTokenizer(layers.Layer):
    """Maps raw features into semantic security tokens."""
    def __init__(self, token_dim=32, **kwargs):
        super().__init__(**kwargs)
        self.token_dim = token_dim
        self.num_tokens = 5
        self.projections = [layers.Dense(token_dim, activation='relu', name=f'token_proj_{i}')
                            for i in range(self.num_tokens)]

    def call(self, inputs):
        tokens = []
        input_dim = tf.shape(inputs)[1]
        for i in range(self.num_tokens):
            start = i * input_dim // self.num_tokens
            end = (i + 1) * input_dim // self.num_tokens if i < self.num_tokens - 1 else input_dim
            segment = inputs[:, start:end]
            tokens.append(self.projections[i](segment))
        return tf.stack(tokens, axis=1)

    def get_config(self):
        config = super().get_config()
        config.update({'token_dim': self.token_dim})
        return config


class RiskGatedSecurityAttention(layers.Layer):
    """Attention mechanism gated by learned risk scores."""
    def __init__(self, token_dim=32, **kwargs):
        super().__init__(**kwargs)
        self.token_dim = token_dim
        self.Wq = layers.Dense(token_dim, name='query_proj')
        self.Wk = layers.Dense(token_dim, name='key_proj')
        self.Wv = layers.Dense(token_dim, name='value_proj')
        self.W_int = layers.Dense(1, use_bias=False, name='interaction_kernel')
        self.risk_gate = layers.Dense(1, activation='sigmoid', name='risk_gate')

    def call(self, tokens):
        Q, K, V = self.Wq(tokens), self.Wk(tokens), self.Wv(tokens)
        num_tokens = tf.shape(tokens)[1]
        Q_exp = tf.tile(tf.expand_dims(Q, 2), [1, 1, num_tokens, 1])
        K_exp = tf.tile(tf.expand_dims(K, 1), [1, num_tokens, 1, 1])
        interaction_scores = self.W_int(tf.concat([Q_exp, K_exp], axis=-1))
        interaction_gate = tf.sigmoid(interaction_scores)
        risk_expanded = tf.expand_dims(self.risk_gate(tokens), axis=2)
        attention_weights = tf.squeeze(interaction_gate * risk_expanded, axis=-1)
        return tf.matmul(attention_weights, V), attention_weights

    def get_config(self):
        config = super().get_config()
        config.update({'token_dim': self.token_dim})
        return config


def build_rgsa_base(input_dim: int, token_dim: int = None):
    """Construct the shared RGSA base model."""
    token_dim = token_dim or HYPERPARAMS['token_dim']
    inputs = layers.Input(shape=(input_dim,), name='input_features')
    tokens = SecurityTokenizer(token_dim, name='security_tokenizer')(inputs)
    attended, _ = RiskGatedSecurityAttention(token_dim, name='risk_gated_attention')(tokens)
    x = layers.Add(name='attention_residual')([tokens, attended])
    x = layers.LayerNormalization(name='attention_layernorm')(x)
    ff = layers.Dense(token_dim * 2, activation='relu', name='ffn_dense1')(x)
    ff = layers.Dropout(0.3, name='ffn_dropout1')(ff)
    ff = layers.Dense(token_dim, activation='relu', name='ffn_dense2')(ff)
    x = layers.Add(name='ffn_residual')([x, ff])
    x = layers.LayerNormalization(name='ffn_layernorm')(x)
    x = layers.GlobalAveragePooling1D(name='global_pool')(x)
    x = layers.Dense(64, activation='relu', name='dense1')(x)
    x = layers.BatchNormalization(name='bn1')(x)
    x = layers.Dropout(0.4, name='dropout1')(x)
    x = layers.Dense(32, activation='relu', name='dense2')(x)
    x = layers.BatchNormalization(name='bn2')(x)
    x = layers.Dropout(0.3, name='dropout2')(x)
    return Model(inputs, x, name='RGSA_Base')
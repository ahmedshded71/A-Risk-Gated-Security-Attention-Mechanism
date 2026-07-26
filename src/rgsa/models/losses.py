"""Custom loss functions."""
import tensorflow as tf


def sparse_focal_loss(gamma: float = 2.0):
    """Focal loss compatible with sparse integer labels."""
    def loss(y_true, y_pred):
        y_true = tf.squeeze(y_true)
        num_classes = tf.shape(y_pred)[1]
        y_true_one_hot = tf.one_hot(tf.cast(y_true, tf.int32), depth=num_classes)
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        pt = tf.reduce_sum(y_true_one_hot * y_pred, axis=-1)
        focal_weight = tf.pow(1.0 - pt, gamma)
        ce_loss = -tf.math.log(pt)
        return tf.reduce_mean(focal_weight * ce_loss)
    return loss
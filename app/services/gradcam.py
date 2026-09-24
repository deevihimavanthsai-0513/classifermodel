import os
import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "ml" / "saved_model" / "rice_model_mobilenet.h5"

model = load_model(MODEL_PATH)
LAST_CONV_LAYER = "conv_pw_13_relu"


def generate_gradcam(image_path: str, output_path: str):
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (224, 224))

    input_img = img_resized.astype("float32") / 255.0
    input_img = np.expand_dims(input_img, axis=0)

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[model.get_layer(LAST_CONV_LAYER).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_output, predictions = grad_model(input_img)
        
        # Ensure predictions is converted to a Tensor
        if isinstance(predictions, list):
            predictions = predictions[0]

        class_index = tf.argmax(predictions[0])
        loss = tf.gather(predictions[0], class_index)

    grads = tape.gradient(loss, conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_output = conv_output[0]

    # Calculate weighted feature map
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # Convert to NumPy array & normalize
    heatmap = np.maximum(heatmap, 0)
    max_val = np.max(heatmap)
    if max_val != 0:
        heatmap /= max_val

    # Resize directly (heatmap is already a numpy array)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Blend original image with heatmap overlay
    superimposed = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    cv2.imwrite(output_path, superimposed)
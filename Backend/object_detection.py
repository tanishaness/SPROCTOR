import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Load the SSD MobileNet V2 model from TensorFlow Hub
def load_model():
    try:
        model = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print("Error loading model:", e)
        return None

# Function to perform object detection on an image tensor
def detect_objects(model, image):
    # Resize and prepare image tensor
    image_resized = cv2.resize(image, (320, 320))
    input_tensor = tf.convert_to_tensor(image_resized, dtype=tf.uint8)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run inference
    return model(input_tensor)

# Function to map detection class IDs to class names
def get_class_name(class_id, class_names):
    return class_names.get(class_id, "Unknown")

# Draw bounding boxes and labels on the image
def draw_boxes(image, boxes, class_ids, scores, class_names, threshold=0.5):
    height, width, _ = image.shape
    detected_items = []

    for i in range(len(scores)):
        if scores[i] >= threshold:
            box = boxes[i]
            ymin, xmin, ymax, xmax = box
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)
            
            class_name = get_class_name(class_ids[i], class_names)
            confidence = scores[i] * 100

            # Draw bounding box and label
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            label = f"{class_name}: {confidence:.2f}%"
            cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            detected_items.append(class_name)

    print("Detected items:", ", ".join(set(detected_items)))
    return image

# Main function for object detection
def main(image_path, model, class_names, threshold=0.5, save_output=False):
    # Load image
    image = load_image(image_path)
    if image is None:
        print("Error: Could not load image.")
        return

    # Detect objects
    detection = detect_objects(model, image)

    # Extract detection data
    boxes = detection["detection_boxes"].numpy()[0]
    class_ids = detection["detection_classes"].numpy()[0].astype(int)
    scores = detection["detection_scores"].numpy()[0]

    # Draw boxes on image
    image_with_boxes = draw_boxes(image, boxes, class_ids, scores, class_names, threshold)

    # Show and optionally save the output
    cv2.imshow("Object Detection", cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR))
    if save_output:
        cv2.imwrite("output_detected.jpg", cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Run detection with threshold and save option
if __name__ == "__main__":
    class_names = {
        1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 64: 'laptop', 67: 'cell phone'
    }
    model = load_model()
    if model:
        image_path = "test-image2.jpg"  # Adjust image path as needed
        main(image_path, model, class_names, threshold=0.5, save_output=True)

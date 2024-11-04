import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import json

# Function to load the SSD MobileNet V2 model
def load_detector_model():
    return hub.load("https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v2/TensorFlow2/fpnlite-320x320/1")

# Load class names from an external file
with open("class_names.json") as f:
    class_names = json.load(f)

# Function to perform object detection
def detect_objects(model, image):
    # Resize image and maintain aspect ratio
    h, w = image.shape[:2]
    scale_factor = 320 / max(h, w)
    image_resized = cv2.resize(image, (int(w * scale_factor), int(h * scale_factor)))
    input_tensor = tf.convert_to_tensor(image_resized[tf.newaxis, ...], dtype=tf.uint8)

    # Perform inference
    return model(input_tensor)

# Load and preprocess the image
def load_image(image_path):
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Draw boxes with information overlay
def draw_boxes(image, boxes, class_ids, scores, threshold=0.5):
    h, w, _ = image.shape
    detected_items = set()

    for box, class_id, score in zip(boxes, class_ids, scores):
        if score >= threshold:
            # Rescale bounding box coordinates
            ymin, xmin, ymax, xmax = [int(val * dim) for val, dim in zip(box, [h, w, h, w])]

            # Retrieve class name
            class_name = class_names.get(str(class_id), 'Unknown')
            print(f"Detected: {class_name}, Confidence: {score:.2%}")

            # Draw bounding box and label on image
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.putText(image, f"{class_name} ({score:.2f})", (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Track detected specific items
            if class_id in {64, 67}:  # 64: 'Laptop', 67: 'Cell Phone'
                detected_items.add(class_name)

    # Log the detected items if any
    print("Found:", ", ".join(detected_items) if detected_items else "None")
    return image

# Main function to execute the detection
def main(image_path, threshold=0.5):
    model = load_detector_model()
    image = load_image(image_path)
    detector_output = detect_objects(model, image)

    # Extract bounding boxes, classes, and scores
    boxes = detector_output["detection_boxes"].numpy()[0]
    class_ids = detector_output["detection_classes"].numpy()[0].astype(int)
    scores = detector_output["detection_scores"].numpy()[0]

    # Draw boxes on the image
    image_with_boxes = draw_boxes(image, boxes, class_ids, scores, threshold)

    # Display the image if environment allows
    if "DISPLAY" in os.environ:  # Check if display is available (e.g., on local machines)
        cv2.imshow("Object Detection", cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Run the main function
if __name__ == "__main__":
    image_path = "test-image2.jpg"  # Change this to your image path
    main(image_path)

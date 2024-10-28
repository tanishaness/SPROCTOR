import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

# Load the SSD MobileNet V2 model from TensorFlow Hub
detector = hub.load("https://www.kaggle.com/models/tensorflow/ssd-mobilenet-v2/TensorFlow2/fpnlite-320x320/1")

# Mapping class IDs to class names for COCO dataset
class_names = {
    1: 'person',
    2: 'bicycle',
    3: 'car',
    4: 'motorcycle',
    5: 'airplane',
    6: 'bus',
    7: 'train',
    8: 'truck',
    9: 'boat',
    10: 'traffic light',
    11: 'fire hydrant',
    12: 'stop sign',
    13: 'parking meter',
    14: 'bench',
    15: 'bird',
    16: 'cat',
    17: 'dog',
    18: 'horse',
    19: 'sheep',
    20: 'cow',
    21: 'elephant',
    22: 'bear',
    23: 'zebra',
    24: 'giraffe',
    25: 'backpack',
    26: 'umbrella',
    27: 'handbag',
    28: 'tie',
    29: 'suitcase',
    30: 'frisbee',
    31: 'skis',
    32: 'snowboard',
    33: 'sports ball',
    34: 'kite',
    35: 'baseball bat',
    36: 'baseball glove',
    37: 'skateboard',
    38: 'surfboard',
    39: 'tennis racket',
    40: 'bottle',
    41: 'wine glass',
    42: 'cup',
    43: 'fork',
    44: 'knife',
    45: 'spoon',
    46: 'bowl',
    47: 'banana',
    48: 'apple',
    49: 'sandwich',
    50: 'orange',
    51: 'broccoli',
    52: 'carrot',
    53: 'hot dog',
    54: 'pizza',
    55: 'donut',
    56: 'cake',
    57: 'chair',
    58: 'couch',
    59: 'potted plant',
    60: 'bed',
    61: 'dining table',
    62: 'toilet',
    63: 'TV',
    64: 'laptop',
    65: 'mouse',
    66: 'remote',
    67: 'keyboard',
    68: 'cell phone',
    69: 'microwave',
    70: 'oven',
    71: 'toaster',
    72: 'sink',
    73: 'refrigerator',
    74: 'book',
    75: 'clock',
    76: 'vase',
    77: 'scissors',
    78: 'teddy bear',
    79: 'hair drier',
    80: 'toothbrush'
}

# Function to perform object detection
def detect_objects(image):
    # Convert the image to a tensor and resize it
    image_resized = cv2.resize(image, (320, 320))  # Resize to model input size
    input_tensor = tf.convert_to_tensor(image_resized)
    input_tensor = input_tensor[tf.newaxis, ...]  # Add batch dimension

    # Perform inference
    detector_output = detector(input_tensor)

    return detector_output

def load_image(image_path):
    # Load an image from a file path
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def draw_boxes(image, boxes, class_ids, scores, threshold=0.5):
    height, width, _ = image.shape
    found_items = []  # List to store found items

    for i in range(len(scores)):
        if scores[i] > threshold:
            box = boxes[i]
            (ymin, xmin, ymax, xmax) = box
            # Scale bounding box to original image dimensions
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)

            # Get class name from class ID
            class_name = class_names.get(class_ids[i], 'Unknown')

            # Print class name and confidence score
            print(f'Detected Class: {class_name}, Confidence: {scores[i] * 100:.2f}%')

            # Check if the detected object is a laptop or a cell phone
            if class_ids[i] == 64:  # Class ID for 'laptop'
                found_items.append('Laptop')
            elif class_ids[i] == 67:  # Class ID for 'cell phone'
                found_items.append('Cell Phone')

            # Draw bounding box
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.putText(image, f'{class_name} ({scores[i]:.2f})', 
                        (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    
    # Print found items
    if found_items:
        print("Found:", ", ".join(set(found_items)))  # Print unique found items
    else:
        print("None")

    return image

# Main function to execute the detection
def main(image_path):
    image = load_image(image_path)
    detector_output = detect_objects(image)

    # Extract data from detector output
    boxes = detector_output["detection_boxes"].numpy()[0]  # Bounding boxes
    class_ids = detector_output["detection_classes"].numpy()[0].astype(int)  # Class IDs
    scores = detector_output["detection_scores"].numpy()[0]  # Confidence scores

    # Draw bounding boxes on the image
    image_with_boxes = draw_boxes(image, boxes, class_ids, scores)

    # Display the image
    cv2.imshow('Object Detection', cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Call the main function with the path to your image
image_path = "test-image2.jpg"  # Change this to your image path
main(image_path)

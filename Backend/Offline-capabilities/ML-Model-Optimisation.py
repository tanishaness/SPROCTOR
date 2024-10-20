import tensorflow as tf
import tensorflow.lite as tflite

# Load the TensorFlow Lite model
def load_tflite_model(model_path):
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    return interpreter

# Sample cheat detection using the lightweight model
def detect_cheating_tflite(frame, interpreter):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Preprocess the frame (resize, normalize, etc.)
    input_data = preprocess_frame_for_model(frame)

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run inference
    interpreter.invoke()

    # Get the result
    cheat_probability = interpreter.get_tensor(output_details[0]['index'])
    return cheat_probability

def preprocess_frame_for_model(frame):
    # Example preprocessing step (adjust according to your model)
    frame_resized = cv2.resize(frame, (224, 224))
    frame_normalized = frame_resized / 255.0
    return frame_normalized.reshape(1, 224, 224, 3).astype('float32')

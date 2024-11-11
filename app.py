from flask import Flask, request, render_template, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the pre-trained model
model = tf.keras.models.load_model("cheat_detector_model.h5")

# Define the path to save uploaded images
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Preprocess the image for prediction
def prepare_image(image_path):
    img = load_img(
        image_path, target_size=(150, 150)
    )  # Resize as per model input shape
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize if required by the model
    return img_array


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Preprocess the image and make prediction
            img_array = prepare_image(filepath)
            prediction = model.predict(img_array)[0][0]

            # Classify as "Cheating" or "Not Cheating"
            if prediction > 0.5:  # Adjust threshold as needed
                result = "Cheating"
            else:
                result = "Not Cheating"

            # Remove the saved image after prediction
            os.remove(filepath)

            # Return result as JSON
            return jsonify({"result": result, "confidence": float(prediction)})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from keras.utils import load_img, img_to_array
from keras.models import load_model

import numpy as np
import os

class_names = {
    0: "Pepper bell Bacterial_spot (alt)",
    1: "Pepper bell healthy",
    2: "Potato Early blight",
    3: "Potato Late blight",
    4: "Potato healthy",
    5: "Tomato Bacterial spot",
    6: "Tomato Early blight",
    7: "Tomato Late blight",
    8: "Tomato Leaf Mold",
    9: "Tomato Septoria leaf spot",
    10: "Tomato Spider mites Two spotted spider mite",
    11: "Tomato Target_Spot",
    12: "Tomato YellowLeaf Curl Virus",
    13: "Tomato mosaic virus",
    14: "Tomato healthy",
}

remedies = {
    0: [
        "Remove and destroy infected plant parts.",
        "Apply copper-based fungicides or bactericides following label instructions.",
        "Rotate crops and practice good sanitation.",
    ],
    2: [
        "Remove and destroy infected leaves and plant debris.",
        "Apply fungicides containing chlorothalonil or copper-based fungicides following label instructions.",
        "Practice crop rotation and avoid overhead irrigation.",
    ],
    3: [
        "Remove and destroy infected plants and tubers.",
        "Apply fungicides containing chlorothalonil or copper-based fungicides following label instructions.",
        "Practice crop rotation and provide good airflow.",
    ],
    5: [
        "Remove and destroy infected plant parts.",
        "Apply copper-based bactericides following label instructions.",
        "Practice crop rotation and avoid overhead watering.",
    ],
    6: [
        "Remove and destroy infected leaves and plant debris.",
        "Apply fungicides containing chlorothalonil or copper-based fungicides following label instructions.",
        "Practice crop rotation, provide good airflow, and avoid overhead watering.",
    ],
    7: [
        "Remove and destroy infected plants and fruit.",
        "Apply fungicides containing chlorothalonil or copper-based fungicides following label instructions.",
        "Practice crop rotation, provide good airflow, and avoid overhead watering.",
    ],
    8: [
        "Remove and destroy infected leaves and plant debris.",
        "Provide good airflow and ventilation to reduce humidity.",
        "Avoid overhead watering and apply fungicides if necessary.",
    ],
    9: [
        "Remove and destroy infected leaves and plant debris.",
        "Apply fungicides containing chlorothalonil or copper-based fungicides following label instructions.",
        "Practice crop rotation, provide good airflow, and avoid overhead watering.",
    ],
    10: [
        "Spray affected plants with a strong jet of water to dislodge mites.",
        "Apply insecticidal soap or horticultural oil following label instructions.",
        "Introduce beneficial predatory mites or other natural enemies to control the population.",
    ],
    11: [
        "Remove and destroy infected leaves and plant debris.",
        "Apply fungicides containing chlorothalonil or copper-based fungicides following label instructions.",
        "Practice crop rotation, provide good airflow, and avoid overhead watering.",
    ],
    12: [
        "Plant resistant varieties if available.",
        "Control whiteflies, which spread the virus, using sticky traps or insecticides.",
        "Remove and destroy infected plants.",
    ],
    13: [
        "Plant resistant varieties if available.",
        "Control aphids, which transmit the virus, using insecticides or reflective mulches.",
        "Remove and destroy infected plants.",
    ],
}

model = load_model("model/vgg16_model.h5")
# model = load_model("model/vgg16_model.h5")
# model = load_model("model/inceptionv3_finetuned_model.h5")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("index.html")

    file = request.files["file"]
    file_extension = os.path.splitext(file.filename)[1]
    newfilename = "uploaded" + file_extension
    img_path = "static/images/uploads/" + newfilename
    file.save(img_path)

    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x /= 255.0
    x = np.expand_dims(x, axis=0)

    predictions = model.predict(x)
    class_idx = np.argmax(predictions[0])
    confidence_score = predictions[0][class_idx] * 100

    ## confidence scores 
    # for i, pred in enumerate(predictions[0]):
    #     class_label = class_names[i]
    #     confidence = pred * 100
    #     print(f"{class_label}: {confidence:.2f}%")

    print("confidence: ", confidence_score)
    confidence = "{:.2f}".format(confidence_score)

    if class_idx == 14 or class_idx == 4 or class_idx == 1:
        predicted_disease = "No disease detected (Healthy Leaf)"
        treatment = []
    else:
        predicted_disease = class_names[class_idx]
        treatment = remedies[class_idx]

    return render_template(
        "result.html",
        confidence=confidence,
        filename=newfilename,
        predicted_disease=predicted_disease,
        treatment=treatment,
    )


@app.errorhandler(Exception)
def handle_exception(error):
    print(error)
    return render_template("error.html", error=error), 500


if __name__ == "__main__":
    app.run()

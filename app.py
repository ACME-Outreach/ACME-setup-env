import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import tensorflow as tf

# Create the Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- CNN Model Loading ---
# Load your trained model here
# model = tf.keras.models.load_model('skin_analysis_model.h5')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # --- Image Preprocessing and Prediction ---
            # img = Image.open(filepath).resize((128, 128))
            # img_array = np.array(img) / 255.0
            # img_array = np.expand_dims(img_array, axis=0)

            # predictions = model.predict(img_array)
            # melanin_prediction = predictions[0][0][0]
            # sebum_prediction = predictions[1][0][0]

            # For now, using dummy predictions
            melanin_prediction = 0.5
            sebum_prediction = 0.3


            return render_template('index.html', filename=filename, melanin=melanin_prediction, sebum=sebum_prediction)
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)

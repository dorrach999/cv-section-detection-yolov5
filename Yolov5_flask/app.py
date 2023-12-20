from flask import Flask, request, render_template
import argparse
import io
from PIL import Image
import datetime

import torch
import cv2
import numpy as np
import tensorflow as tf
from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
from subprocess import Popen
import re
import requests
import shutil
import time


app = Flask(__name__)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best1.pt', force_reload=True)
# Set the confidence threshold (e.g., 0.15)
confidence_threshold = 0.2

# Adjust confidence threshold in the model
model.conf = confidence_threshold

model.eval()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle the uploaded image
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            # Save the uploaded file
            image_path = 'static/uploaded_image.jpg'
            file.save(image_path)

            # Perform inference on the image
            results = model(image_path)

            # Get the annotated image with blocks only
            annotated_image = Image.fromarray(results.render()[0])

            # Save the annotated image
            annotated_image_path = 'static/annotated_image.jpg'
            annotated_image.save(annotated_image_path)


            # Display the annotated image with blocks only
            return render_template('index.html', annotated_image_path=annotated_image_path)

    return render_template('index.html')

if __name__ == '__main__':
     app.run(port=5000)

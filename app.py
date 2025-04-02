import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import io
import base64

from disease_detector import analyze_image, get_disease_info, common_diseases

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure uploads
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file was uploaded
    if 'file' not in request.files:
        if 'image_data' in request.form:
            # Handle base64 image data from camera capture
            try:
                image_data = request.form['image_data']
                # Remove data:image/jpeg;base64, prefix if it exists
                if 'base64,' in image_data:
                    image_data = image_data.split('base64,')[1]
                
                # Decode the base64 image
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                
                # Save to a temporary file
                temp_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.jpg')
                image.save(temp_filename)
                
                # Process the image
                return process_image(temp_filename)
            except Exception as e:
                app.logger.error(f"Error processing captured image: {e}")
                flash('Error processing the captured image', 'error')
                return redirect(url_for('index'))
        else:
            flash('No file selected for uploading', 'error')
            return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if file has name and is allowed
    if file.filename == '':
        flash('No file selected for uploading', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return process_image(filepath)
        except Exception as e:
            app.logger.error(f"Error processing uploaded file: {e}")
            flash('Error processing the uploaded file', 'error')
            return redirect(url_for('index'))
    else:
        flash('Allowed file types are png, jpg, jpeg', 'error')
        return redirect(url_for('index'))

def process_image(filepath):
    try:
        # Open and analyze the image
        with Image.open(filepath) as img:
            # Ensure the image is in RGB format
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize for analysis if needed
            analysis_img = img.copy()
            if max(analysis_img.size) > 1024:
                analysis_img.thumbnail((1024, 1024))
            
            # Analyze the image
            disease_id, confidence, affected_areas = analyze_image(np.array(analysis_img))
            
            # Get disease information
            disease_info = get_disease_info(disease_id)
            
            # Save processed image with highlighted areas
            base_img = img.copy()
            if max(base_img.size) > 800:  # Resize for display
                base_img.thumbnail((800, 800))
            
            # Convert the image to base64 for embedding in HTML
            buffered = io.BytesIO()
            base_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Store results in session
            session['analysis_results'] = {
                'image': img_str,
                'disease_id': disease_id,
                'disease_name': disease_info['name'],
                'confidence': f"{confidence:.1f}%",
                'description': disease_info['description'],
                'treatment': disease_info['treatment'],
                'prevention': disease_info['prevention'],
                'affected_areas': affected_areas
            }
            
            return redirect(url_for('results'))
    except Exception as e:
        app.logger.error(f"Error in image processing: {e}")
        flash('Error processing the image. Please try another image.', 'error')
        return redirect(url_for('index'))

@app.route('/results')
def results():
    if 'analysis_results' not in session:
        flash('No image has been analyzed. Please upload an image first.', 'warning')
        return redirect(url_for('index'))
    
    results = session['analysis_results']
    return render_template('results.html', results=results)

@app.route('/browse')
def browse_diseases():
    return render_template('browse_diseases.html', diseases=common_diseases)

@app.route('/api/disease/<int:disease_id>')
def disease_api(disease_id):
    disease_info = get_disease_info(disease_id)
    if disease_info:
        return jsonify(disease_info)
    return jsonify({"error": "Disease not found"}), 404

@app.errorhandler(413)
def too_large(e):
    flash('The file is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {e}")
    flash('An unexpected error occurred. Please try again later.', 'error')
    return redirect(url_for('index'))

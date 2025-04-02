
from http.client import HTTPException

# Vercel serverless handler
def handler(request):
    try:
        return app(request)
    except HTTPException as e:
        return e
    except Exception as e:
        app.logger.error(f"Unhandled error: {e}")
        return "Internal Server Error", 500


import os
import logging
import uuid
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
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
# Use /tmp directory for Vercel serverless environment
is_vercel = os.environ.get('VERCEL', 'false') == 'true'
UPLOAD_FOLDER = '/tmp/uploads' if is_vercel else './uploads'
RESULTS_FOLDER = '/tmp/results' if is_vercel else './results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure directories exist
try:
    for folder in [UPLOAD_FOLDER, RESULTS_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
except Exception as e:
    logging.error(f"Failed to create directory: {e}")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    try:
        app.logger.debug("Rendering index template")
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Error rendering index template: {e}")
        return f"Error: {e}", 500

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
        # Open and analyze the image - optimize by using a single image object
        with Image.open(filepath) as img:
            # Ensure the image is in RGB format
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create a smaller version for analysis (faster processing)
            analysis_size = (512, 512)  # Reduced size for faster analysis
            analysis_img = img.copy()
            analysis_img.thumbnail(analysis_size)
            
            # Analyze the image
            disease_id, confidence, affected_areas = analyze_image(np.array(analysis_img))
            
            # Get disease information
            disease_info = get_disease_info(disease_id)
            
            # Ensure disease_info is not None to avoid 'not subscriptable' errors
            if disease_info is None:
                # Default to the "Healthy Plant" entry if disease info is not found
                disease_info = {
                    'id': 6,
                    'name': 'Healthy Plant',
                    'crops': ['Various'],
                    'description': 'This plant appears healthy with no visible signs of disease or pest damage.',
                    'treatment': 'No treatment needed. Continue with regular care practices.',
                    'prevention': 'Maintain good cultural practices including proper watering, fertilization, and pest monitoring.'
                }
            
            # Create a smaller version for display (faster loading)
            display_size = (600, 600)  # Reduced size for faster display
            display_img = img.copy()
            display_img.thumbnail(display_size)
            
            # Generate a unique ID for this analysis
            result_id = str(uuid.uuid4())
            
            # Save the processed image to disk instead of session
            result_filename = f"{result_id}.jpg"
            result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
            display_img.save(result_path, format="JPEG", quality=85, optimize=True)
            
            # Store minimal results in session (no image data)
            session['analysis_results'] = {
                'result_id': result_id,
                'disease_id': disease_info['id'],
                'disease_name': disease_info['name'],
                'confidence': f"{confidence:.1f}%",
                'description': disease_info['description'],
                'treatment': disease_info['treatment'],
                'prevention': disease_info['prevention'],
                'affected_areas': affected_areas
            }
            
            # Clean up temporary files to save disk space
            try:
                os.remove(filepath)
            except:
                pass
                
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

@app.route('/results/image/<result_id>')
def result_image(result_id):
    # Validate the result_id to prevent directory traversal
    if not result_id or '..' in result_id or '/' in result_id:
        return "Invalid result ID", 400
        
    image_path = os.path.join(app.config['RESULTS_FOLDER'], f"{result_id}.jpg")
    
    if not os.path.exists(image_path):
        return "Image not found", 404
        
    return send_file(image_path, mimetype='image/jpeg')

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

# Background cleanup process
def cleanup_old_files():
    """Clean up old image files to prevent disk space issues"""
    while True:
        try:
            # Wait for 1 hour between cleanups
            time.sleep(3600)
            
            now = datetime.now()
            count = 0
            
            # Clean up results folder (keep files for 24 hours)
            for filename in os.listdir(app.config['RESULTS_FOLDER']):
                filepath = os.path.join(app.config['RESULTS_FOLDER'], filename)
                
                # Skip if not a file
                if not os.path.isfile(filepath):
                    continue
                    
                # Get file modification time
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # Remove if older than 24 hours
                if now - file_time > timedelta(hours=24):
                    try:
                        os.remove(filepath)
                        count += 1
                    except Exception as e:
                        app.logger.error(f"Error removing old file {filepath}: {e}")
            
            app.logger.info(f"Cleanup complete. Removed {count} old image files.")
            
        except Exception as e:
            app.logger.error(f"Error in cleanup process: {e}")

# Start the background cleanup thread only in non-Vercel environments
# Vercel uses serverless functions which don't support long-running processes
if not is_vercel:
    cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
    cleanup_thread.start()

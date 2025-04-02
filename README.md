# Plant Disease Detection System

A web-based application that analyzes plant images to identify diseases and provide treatment recommendations.

## Features

- **Image Upload**: Upload plant images for analysis
- **Camera Capture**: Take photos directly from your device camera
- **Disease Detection**: Identify plant diseases with confidence levels
- **Treatment Information**: Get detailed information about detected diseases
- **Prevention Tips**: Learn how to prevent plant diseases
- **Disease Library**: Browse common plant diseases and their treatments

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Image Processing**: NumPy, Pillow
- **UI Design**: Clean, responsive interface with accessibility features

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py` - Main Flask application with routes and controllers
- `disease_detector.py` - Image analysis and disease detection logic
- `main.py` - Application entry point
- `models.py` - Data models (if using a database)
- `templates/` - HTML templates for the application
- `static/` - CSS, JavaScript and image assets
- `uploads/` - Temporary storage for uploaded images
- `results/` - Storage for processed analysis results

## Screenshot

![Plant Disease Detection System](https://example.com/screenshot.jpg)

## Future Enhancements

- Integration with a real machine learning model for more accurate disease detection
- User accounts to track plant health history
- Mobile application version
- Expanded disease database
- Integration with weather APIs for contextual advice
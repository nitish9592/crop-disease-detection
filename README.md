# Crop Disease Detection System

A web-based crop disease detection system that analyzes plant images to identify diseases and provide information about treatment and prevention.

## Features

- Upload or capture plant images for disease detection
- Real-time image analysis with disease identification
- Detailed information on detected diseases with treatment recommendations
- Browse common plant diseases library
- Responsive design for mobile and desktop use

## Technology Stack

- Python/Flask backend
- HTML, CSS, JavaScript for the frontend
- Bootstrap for responsive design
- Pillow and NumPy for image processing

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/nitish9592/crop-disease-detection.git
cd crop-disease-detection
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

1. Upload a plant image using the file uploader or capture one using your device camera
2. The system will analyze the image and identify any diseases
3. Review the analysis results with highlighted affected areas
4. Get information about the detected disease and treatment recommendations
5. Browse the disease library to learn about common plant diseases

## Project Structure

- `app.py`: Main Flask application with routes
- `disease_detector.py`: Contains functions for plant disease detection
- `main.py`: Entry point for the application
- `templates/`: HTML templates for the web interface
- `static/`: Static assets (CSS, JavaScript, images)

## License

MIT License
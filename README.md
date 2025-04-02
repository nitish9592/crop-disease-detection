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

### Local Development

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

### Vercel Deployment

1. Fork or clone this repository to your GitHub account
2. Create a new project in Vercel and connect your GitHub repository
3. Set deployment settings:
   - Framework: Other
   - Build Command: (leave blank)
   - Output Directory: (leave blank)
4. Add Environment Variable:
   - Key: `SESSION_SECRET`
   - Value: (a secure random string)
5. Click "Deploy"

#### Notes on Vercel Serverless Functions

The application is adapted to work in Vercel's serverless environment with the following considerations:
- File storage uses `/tmp` directory which has limitations on space and persistence
- Long-running background processes are disabled in serverless mode
- Session data should be kept minimal due to size constraints
- Cold starts may cause initial latency for first-time users

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
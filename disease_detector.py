import numpy as np
from PIL import Image, ImageDraw
import io
import base64
import random

# This is a simplified implementation for demonstration purposes
# In a real-world scenario, this would use a trained ML model

# Common crop diseases database
common_diseases = [
    {
        'id': 1,
        'name': 'Late Blight',
        'crops': ['Potato', 'Tomato'],
        'description': 'Late blight is a plant disease caused by the oomycete Phytophthora infestans. Symptoms include dark lesions on leaves and stems that spread quickly in cool, wet conditions.',
        'treatment': 'Apply fungicides with active ingredients such as chlorothalonil, mancozeb, or copper-based compounds. Remove and destroy infected plant parts.',
        'prevention': 'Use resistant varieties, ensure proper spacing for air circulation, avoid overhead irrigation, and practice crop rotation.'
    },
    {
        'id': 2,
        'name': 'Powdery Mildew',
        'crops': ['Wheat', 'Barley', 'Grape', 'Cucumber'],
        'description': 'Powdery mildew is a fungal disease that causes a white powdery substance on leaf surfaces, stems, and sometimes fruit. It can reduce photosynthesis and yield.',
        'treatment': 'Apply sulfur-based fungicides or neem oil. Prune affected parts and ensure good air circulation.',
        'prevention': 'Plant resistant varieties, avoid overcrowding, and reduce humidity around plants.'
    },
    {
        'id': 3,
        'name': 'Apple Scab',
        'crops': ['Apple'],
        'description': 'Apple scab is a fungal disease causing dark, scabby lesions on leaves and fruit. Severe infections can lead to defoliation and unmarketable fruit.',
        'treatment': 'Apply fungicides like captan or myclobutanil. Remove fallen leaves and infected fruit.',
        'prevention': 'Plant resistant varieties, practice good orchard sanitation, and ensure proper pruning for airflow.'
    },
    {
        'id': 4,
        'name': 'Citrus Greening',
        'crops': ['Orange', 'Lemon', 'Lime', 'Grapefruit'],
        'description': 'Citrus greening (Huanglongbing) is a bacterial disease spread by psyllids. It causes mottled leaves, misshapen fruit, and eventually tree death.',
        'treatment': 'No cure available. Remove infected trees to prevent spread.',
        'prevention': 'Control psyllid populations, use disease-free planting material, and monitor trees regularly.'
    },
    {
        'id': 5,
        'name': 'Corn Gray Leaf Spot',
        'crops': ['Corn', 'Maize'],
        'description': 'Gray leaf spot is a fungal disease causing rectangular, gray-brown lesions on corn leaves. Severe cases lead to significant yield loss.',
        'treatment': 'Apply fungicides containing strobilurins or triazoles.',
        'prevention': 'Plant resistant hybrids, rotate crops, and practice conservation tillage.'
    },
    {
        'id': 6,
        'name': 'Healthy Plant',
        'crops': ['Various'],
        'description': 'This plant appears healthy with no visible signs of disease or pest damage.',
        'treatment': 'No treatment needed. Continue with regular care practices.',
        'prevention': 'Maintain good cultural practices including proper watering, fertilization, and pest monitoring.'
    }
]

def analyze_image(image_array):
    """
    Analyze an image to detect plant diseases.
    
    In a real implementation, this would use a trained machine learning model.
    For demo purposes, we'll simulate disease detection.
    
    Args:
        image_array: NumPy array of the image
        
    Returns:
        disease_id: ID of the detected disease
        confidence: Confidence level (percentage)
        affected_areas: Coordinates of affected areas for highlighting
    """
    # Simple color-based heuristic for demo purposes
    # Green is healthy, brown/yellow/black spots might indicate disease
    
    # Convert image to HSV for better color analysis
    # In a real model, we'd use features extracted by CNN layers
    
    # This is a placeholder implementation
    # Randomly select a disease or healthy status for demo
    if random.random() > 0.3:  # 70% chance of detecting a disease
        disease_id = random.randint(1, 5)  # Random disease from our database
        confidence = random.uniform(70, 95)  # Random confidence between 70-95%
        
        # Generate some random affected areas (x, y, width, height)
        # In a real implementation, these would come from a segmentation model
        h, w = image_array.shape[:2]
        num_areas = random.randint(2, 6)
        affected_areas = []
        
        for _ in range(num_areas):
            x = random.randint(0, w - 100)
            y = random.randint(0, h - 100)
            width = random.randint(50, 100)
            height = random.randint(50, 100)
            affected_areas.append((x, y, width, height))
    else:
        # Healthy plant
        disease_id = 6  # ID for healthy plant
        confidence = random.uniform(80, 98)
        affected_areas = []
    
    return disease_id, confidence, affected_areas

def get_disease_info(disease_id):
    """Get information about a disease from its ID"""
    for disease in common_diseases:
        if disease['id'] == disease_id:
            return disease
    return None

def highlight_affected_areas(image_path, affected_areas):
    """
    Highlight affected areas on an image
    
    Args:
        image_path: Path to the image file
        affected_areas: List of tuples (x, y, width, height)
        
    Returns:
        Base64 encoded image with highlighted areas
    """
    # Open the image
    img = Image.open(image_path)
    
    # Create a drawing context
    draw = ImageDraw.Draw(img)
    
    # Draw rectangles around affected areas
    for x, y, width, height in affected_areas:
        draw.rectangle([(x, y), (x + width, y + height)], outline="red", width=3)
    
    # Convert to base64
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

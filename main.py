from app import app

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
# This module exports the app object for Vercel serverless deployment

document.addEventListener('DOMContentLoaded', function() {
    // Variables for camera functionality
    let stream = null;
    let facingMode = 'environment'; // Start with back camera
    let videoElement = document.getElementById('camera-preview');
    let canvasElement = document.getElementById('capture-canvas');
    let capturedImageContainer = document.getElementById('captured-image-container');
    let capturedImage = document.getElementById('captured-image');
    let captureBtn = document.getElementById('capture-btn');
    let retakeBtn = document.getElementById('retake-btn');
    let useImageBtn = document.getElementById('use-image-btn');
    let switchCameraBtn = document.getElementById('switch-camera-btn');
    let cameraBtn = document.getElementById('camera-btn');
    let cameraModal = null;

    // Initialize the camera modal if elements exist
    if (cameraBtn && videoElement) {
        cameraModal = new bootstrap.Modal(document.getElementById('cameraModal'));
        
        // Open camera when the camera button is clicked
        cameraBtn.addEventListener('click', function() {
            openCamera();
            cameraModal.show();
        });
        
        // Handle camera modal close - stop the stream
        document.getElementById('cameraModal').addEventListener('hidden.bs.modal', function () {
            stopCamera();
        });
        
        // Switch camera button event
        if (switchCameraBtn) {
            switchCameraBtn.addEventListener('click', function() {
                facingMode = facingMode === 'environment' ? 'user' : 'environment';
                stopCamera();
                openCamera();
            });
        }
        
        // Capture button event
        if (captureBtn) {
            captureBtn.addEventListener('click', captureImage);
        }
        
        // Retake button event
        if (retakeBtn) {
            retakeBtn.addEventListener('click', function() {
                capturedImageContainer.style.display = 'none';
                videoElement.style.display = 'block';
                captureBtn.style.display = 'inline-block';
                switchCameraBtn.style.display = 'inline-block';
                retakeBtn.style.display = 'none';
                useImageBtn.style.display = 'none';
            });
        }
        
        // Use image button event
        if (useImageBtn) {
            useImageBtn.addEventListener('click', function() {
                // Get the base64 image data
                const canvas = document.getElementById('capture-canvas');
                const imageData = canvas.toDataURL('image/jpeg');
                
                // Set the image data to the hidden form input
                document.getElementById('image-data-input').value = imageData;
                
                // Submit the form
                document.getElementById('camera-capture-form').submit();
                
                // Show loading state
                const loadingOverlay = document.createElement('div');
                loadingOverlay.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center';
                loadingOverlay.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
                loadingOverlay.style.zIndex = '9999';
                
                const spinner = document.createElement('div');
                spinner.className = 'spinner-border text-primary';
                spinner.setAttribute('role', 'status');
                
                const loadingText = document.createElement('span');
                loadingText.className = 'ms-3';
                loadingText.textContent = 'Analyzing image...';
                
                const loadingContainer = document.createElement('div');
                loadingContainer.className = 'd-flex flex-column align-items-center';
                loadingContainer.appendChild(spinner);
                loadingContainer.appendChild(loadingText);
                
                loadingOverlay.appendChild(loadingContainer);
                document.body.appendChild(loadingOverlay);
                
                // Close the modal
                cameraModal.hide();
            });
        }
    }

    // Function to open the camera
    function openCamera() {
        // Check if the browser supports getUserMedia
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert('Your browser does not support camera access. Please try uploading an image instead.');
            return;
        }
        
        // Get camera stream
        const constraints = {
            video: {
                facingMode: facingMode,
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        };
        
        navigator.mediaDevices.getUserMedia(constraints)
            .then(function(mediaStream) {
                stream = mediaStream;
                videoElement.srcObject = mediaStream;
                videoElement.play();
                videoElement.style.display = 'block';
                capturedImageContainer.style.display = 'none';
                captureBtn.style.display = 'inline-block';
                switchCameraBtn.style.display = 'inline-block';
                retakeBtn.style.display = 'none';
                useImageBtn.style.display = 'none';
            })
            .catch(function(err) {
                console.error('Error accessing camera:', err);
                alert('Could not access the camera. Please check your camera permissions or try uploading an image instead.');
            });
    }

    // Function to stop the camera stream
    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(function(track) {
                track.stop();
            });
            stream = null;
        }
    }

    // Function to capture an image from the video stream
    function captureImage() {
        if (!stream) {
            return;
        }
        
        const context = canvasElement.getContext('2d');
        
        // Set canvas dimensions to match video dimensions
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        
        // Draw the current video frame to the canvas
        context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
        
        // Convert canvas to image and display it
        capturedImage.src = canvasElement.toDataURL('image/jpeg');
        
        // Show the captured image, hide the video
        videoElement.style.display = 'none';
        capturedImageContainer.style.display = 'block';
        
        // Change buttons
        captureBtn.style.display = 'none';
        switchCameraBtn.style.display = 'none';
        retakeBtn.style.display = 'inline-block';
        useImageBtn.style.display = 'inline-block';
    }
});

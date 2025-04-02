document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
    
    // File upload preview
    const fileUpload = document.getElementById('file-upload');
    if (fileUpload) {
        fileUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // You could add preview functionality here if needed
                console.log('File selected:', file.name);
            }
        });
    }
    
    // Form submission loader
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            // Display a loading overlay
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
        });
    }
    
    // Handle feedback buttons on results page
    const feedbackButtons = document.querySelectorAll('.feedback-btn');
    if (feedbackButtons.length > 0) {
        feedbackButtons.forEach(button => {
            button.addEventListener('click', function() {
                const feedbackType = this.getAttribute('data-feedback');
                
                // In a real application, you would send this to the server
                console.log('Feedback received:', feedbackType);
                
                // Show thank you message
                const thanksElement = document.getElementById('feedback-thanks');
                if (thanksElement) {
                    thanksElement.style.display = 'block';
                }
                
                // Disable all feedback buttons
                feedbackButtons.forEach(btn => {
                    btn.disabled = true;
                });
            });
        });
    }
});

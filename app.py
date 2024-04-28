from flask import Flask, render_template, request, redirect, url_for  # Import necessary Flask modules
import os  # Import os module for file operations
import json  # Import json module for JSON file operations
from models.model import predictor  # Import predictor function from models.model module

app = Flask(__name__)  # Initialize Flask application

UPLOAD_FOLDER = 'static/uploads'  # Define upload folder path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Define allowed file extensions

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set upload folder in app configuration

def allowed_file(filename):
    """
    Check if the file extension is allowed.

    Parameters:
        filename (str): Name of the file.

    Returns:
        bool: True if extension is allowed, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  # Return True if extension is allowed, False otherwise

@app.route('/')  # Route for the homepage
def index():
    """
    Render the index.html template.

    Returns:
        rendered_template: Rendered HTML template for the homepage.
    """
    return render_template('index.html')  # Render index.html template

@app.route('/upload', methods=['POST'])  # Route for file upload
def upload_file():
    """
    Handle file upload.

    Returns:
        redirect or str: Redirects to uploaded file display or returns an error message.
    """
    
    file = request.files['file']  # Get the file from request
    if file.filename == '':  # If no selected file
        return redirect(request.url)  # Redirect to the same URL
    if file and allowed_file(file.filename):  # If file is selected and file extension is allowed
        filename = file.filename  # Get the filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file to upload folder
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
        with open(os.path.join(base_dir,"models","config.json")) as fp:  # Open config.json file
            data = json.load(fp)  # Load data from JSON file
        
        predictor(os.path.join(app.config['UPLOAD_FOLDER'], filename),data["classes"], data["weights"],data["config"],filename)  # Use predictor function on the uploaded file
        return redirect(url_for('uploaded_file', filename=filename))  # Redirect to uploaded_file route with filename parameter
    else:
        return "Invalid file format. Please upload an image file."  # Return error message for invalid file format

@app.route('/uploads/<filename>')  # Route for displaying uploaded file
def uploaded_file(filename):
    """
    Render the display.html template with uploaded filename.

    Parameters:
        filename (str): Name of the uploaded file.

    Returns:
        rendered_template: Rendered HTML template for displaying the uploaded file.
    """
    return render_template('display.html', filename=filename)  # Render display.html template with filename parameter

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application in debug mode

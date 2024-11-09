from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Dictionary to store emails organized by appName
emails_by_app = {}
new_apps = [{"name": "chatier", "type": "whatsapp", "scale": "8"},{"name": "gmail", "type": "mail", "scale": "8"},{"name": "dummy", "type": "dummy", "scale": "8"}]

# Route to receive and store email
@app.route('/send_email', methods=['POST'])
def send_email():   
    data = request.headers
    app_name = data.get('appName')
    email_from = data.get('from')
    email_to = data.get('to')
    email_text = data.get('text')
    
    # Basic validation
    if not app_name or not email_from or not email_to or not email_text:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Create email data structure
    email = {
        "from": email_from,
        "to": email_to,
        "text": email_text
    }
    
    # Save the email in the list for the specified appName
    if app_name not in emails_by_app:
        emails_by_app[app_name] = []
    emails_by_app[app_name].append(email)
    
    return jsonify({"message": "Email successfully saved"}), 200

# Route for a user to retrieve their emails in a specific app
@app.route('/get_user_emails/<app_name>', methods=['GET'])
def get_user_emails(app_name):
    # Get user_id from query parameters
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id parameter is missing"}), 400
    
    # Retrieve all emails for the application
    emails = emails_by_app.get(app_name, [])
    
    # Filter only emails addressed to the user_id
    user_emails = [email for email in emails if email["to"] == user_id]
    
    return jsonify({"emails": user_emails}), 200

# Route to retrieve the list of available apps
@app.route('/get_apps', methods=['GET'])
def get_apps():
    return jsonify({"apps": new_apps}), 200

# Route to get the app logo (file serving)
@app.route('/get_app_logo/<app_name>', methods=['GET'])
def get_app_logo(app_name):
    # Define the path to the app's logo
    logo_path = os.path.join("apps", f"{app_name}.png")
    
    # Check if the file exists before sending
    if os.path.exists(logo_path):
        return send_from_directory("apps", f"{app_name}.png", mimetype='image/png')
    else:
        return jsonify({"error": "Logo not found"}), 404

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

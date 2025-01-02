from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import requests
from bs4 import BeautifulSoup
from auth import register, login  
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Secure session key
app.secret_key = os.urandom(24)
# Routes for static pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cracc')
def cracc():
    return render_template('cracc.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

@app.route('/donation')
def donation():
    return render_template('donation.html')

# Route for registration
@app.route('/register', methods=['POST'])
def handle_register():
    return register()  # Use the imported register function

# Route for login
@app.route('/login', methods=['POST'])
def handle_login():
    return login()  # Use the imported login function

# Route for dashboard (protected route)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('index'))  # Redirect to the home page
    return render_template('dashboard.html', email=session['email'])

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    
    # Redirect to the home page or login page
    return redirect(url_for('index'))


# Route for content summarization
@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json

    # Validate the input data
    if not data or not data.get('url'):
        return jsonify({"error": "No URL provided."}), 400

    url = data.get('url')
    summary_length = data.get('length', 'medium')  # Default to 'medium' if not provided
    summary_format = data.get('format', 'paragraph')  # Default to 'paragraph' if not provided

    # Fetch the webpage content
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Handle HTTP errors
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to retrieve webpage: {str(e)}"}), 400

    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    if not paragraphs:
        return jsonify({"error": "No content found to summarize."}), 400

    text_content = ' '.join([para.get_text().strip() for para in paragraphs if para.get_text().strip()])

    # Adjust summary length
    if summary_length == 'short':
        text_content = text_content[:200] + "..."  # Short summary
    elif summary_length == 'long':
        text_content = text_content[:1000] + "..."  # Long summary
    else:
        text_content = text_content[:750] + "..."  # Medium summary (default)

    # Format output
    if summary_format == 'bullet':
        # Convert text into bullet points
        sentences = text_content.split('. ')
        summary = ''.join(f"<li>{sentence.strip()}.</li>" for sentence in sentences if sentence.strip())
        summary = f"<ul>{summary}</ul>"
    else:
        # Default to paragraph format
        summary = text_content

    return jsonify({"summary": summary})

if __name__ == '__main__':
    app.run(debug=True)

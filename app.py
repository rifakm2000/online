from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from io import BytesIO

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'database': 'online'
}

# Route to display the upload form
@app.route('/')
def index():
    return render_template('upload.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'profile_pic' not in request.files:
        return "No file uploaded", 400

    file = request.files['profile_pic']
    if file.filename == '':
        return "No file selected", 400

    username = request.form['username']
    profile_pic = file.read()

    # Save to MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(buffered=True)  # Use buffered cursor
    cursor.execute("INSERT INTO users (username, profile_pic) VALUES (%s, %s)", (username, profile_pic))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('profile', username=username))

# Route to display the profile picture
@app.route('/profile/<username>')
def profile(username):
    # Retrieve the profile picture from MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(buffered=True)  # Use buffered cursor
    cursor.execute("SELECT profile_pic FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()  # Fetch the result
    cursor.close()
    connection.close()

    if result and result[0]:
        # Serve the image
        return send_file(BytesIO(result[0]), mimetype='image/jpeg')
    else:
        return "Profile picture not found", 404

if __name__ == '__main__':
    app.run(debug=True)
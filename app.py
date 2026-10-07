from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import storage
import auth
from logger_config import logger

app = Flask(__name__)
logger.info("Cloud File Storage application started")
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt", "zip"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
auth.init_db()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud File Storage</title>
</head>
<body>

<h1>☁️ Cloud File Storage System</h1>

{% if session.get("username") %}

<p>Welcome, <b>{{ session["username"] }}</b>!</p>
<a href="{{ url_for('logout') }}">Logout</a>

<hr>

<h2>Upload a File</h2>

<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Upload File</button>
</form>

{% if message %}
<p>{{ message }}</p>
{% endif %}

<hr>

<h2>Stored Files</h2>

{% if files %}
<ul>
{% for file in files %}
<li>
    {{ file }}
    <a href="{{ url_for('download_file', filename=file) }}">Download</a>
    <a href="{{ url_for('delete_file', filename=file) }}">Delete</a>
</li>
{% endfor %}
</ul>
{% else %}
<p>No files uploaded yet.</p>
{% endif %}

{% else %}

<h2>Login</h2>

<form method="POST" action="{{ url_for('login') }}">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>

<h2>Register</h2>

<form method="POST" action="{{ url_for('register') }}">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Register</button>
</form>

{% if message %}
<p>{{ message }}</p>
{% endif %}

{% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if not session.get("username"):
        return render_template_string(HTML, message="", files=[])

    message = ""

    if request.method == "POST":

        file = request.files.get("file")

        if file and file.filename:

            filename = secure_filename(file.filename)

            if "." not in filename or filename.rsplit(".", 1)[1].lower() not in ALLOWED_EXTENSIONS:
                message = "File type not allowed."
                files = files_db.get_user_files(session["user_id"])
                return render_template_string(HTML, message=message, files=files)

            storage.save_file(file, filename, session["user_id"])

            message = f"File uploaded successfully: {filename}"

        else:
            message = "Please select a file."

    files = storage.list_files()

    return render_template_string(
        HTML,
        message=message,
        files=files
    )


@app.route("/register", methods=["POST"])
def register():

    username = request.form.get("username")
    password = request.form.get("password")

    if auth.create_user(username, password):
        return redirect(url_for("home"))

    return render_template_string(
        HTML,
        message="Username already exists.",
        files=[]
    )


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    user = auth.authenticate_user(username, password)

    if user:
        session["username"] = user[1]
        return redirect(url_for("home"))

    return render_template_string(
        HTML,
        message="Invalid username or password.",
        files=[]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


@app.route("/download/<filename>")
def download_file(filename):

    if not session.get("username"):
        return redirect(url_for("home"))

    user_folder = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(session["user_id"])
    )

    return send_from_directory(
        user_folder,
        filename,
        as_attachment=True
    )


@app.route("/delete/<filename>")
def delete_file(filename):

    if not session.get("username"):
        return redirect(url_for("home"))

    storage.delete_file(filename, session["user_id"])

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

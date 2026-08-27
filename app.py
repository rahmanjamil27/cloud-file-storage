from flask import Flask, request, render_template_string, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud File Storage</title>
</head>

<body>

    <h1>☁️ Cloud File Storage System</h1>

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

                    <a href="{{ url_for('download_file', filename=file) }}">
                        Download
                    </a>

                    <a href="{{ url_for('delete_file', filename=file) }}">
                        Delete
                    </a>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>No files uploaded yet.</p>
    {% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    message = ""

    if request.method == "POST":

        file = request.files.get("file")

        if file and file.filename:

            file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    file.filename
                )
            )

            message = f"File uploaded successfully: {file.filename}"

        else:

            message = "Please select a file."

    files = os.listdir(app.config["UPLOAD_FOLDER"])

    return render_template_string(
        HTML,
        message=message,
        files=files
    )


@app.route("/download/<filename>")
def download_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=True
    )


@app.route("/delete/<filename>")
def delete_file(filename):

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

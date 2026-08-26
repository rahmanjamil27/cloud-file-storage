from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud File Storage</title>
</head>
<body>
    <h1>Cloud File Storage System</h1>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload File</button>
    </form>

    {% if message %}
        <p>{{ message }}</p>
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
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            message = f"File uploaded successfully: {file.filename}"
        else:
            message = "Please select a file."

    return render_template_string(HTML, message=message)


if __name__ == "__main__":
    app.run(debug=True)
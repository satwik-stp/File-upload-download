import os
from flask import Flask,render_template,request,send_from_directory
from werkzeug.utils import secure_filename

upload_path="/Users/satwik/Documents/upload"
app=Flask(__name__)
app.config['UPLOAD_FOLDER']=upload_path

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/", methods=["POST","GET"])
def upload_file():

    if "file" not in request.files:
        return render_template("start.html", error="No file")

    input = request.files["file"]

    if input.filename == "":
        return render_template("start.html", error="Empty file")

    if input:
        filename = secure_filename(input.filename)
        input.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        stat = os.stat(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return render_template("function.html", result=input.filename, size=stat.st_size)
    else:
        return render_template("start.html", error="Error has occurred")

@app.route("/view", methods=["POST", "GET"])
def view_files():
    list1 = []
    for filename in os.listdir(upload_path):
        path = os.path.join(upload_path, filename)
        if os.path.isfile(path):
            list1.append(filename)
    return render_template("list.html", result=list1)

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__=="__main__":
    app.run(host= "10.2.193.187",port=5005)
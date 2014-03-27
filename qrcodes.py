from bs4 import BeautifulSoup as Soup
import json
import requests
import os
from urllib import quote_plus

from flask import request, Flask, make_response, redirect
from werkzeug.utils import secure_filename

with open('config.json') as f:
    config = json.loads(f.read())

UPLOAD_FOLDER = config["upload_dest"]
if not os.path.exists(UPLOAD_FOLDER):
    print "UPLOADS WILL NOT SUCCEED"
    print UPLOAD_FOLDER + " doesn't exist, you need to fix this. Ctrl+C, mkdir " + UPLOAD_FOLDER + ", then restart the program."
UPLOAD_WEB_ACCESS = config["upload_web_access"]
ALLOWED_EXTENSIONS = set(config["extensions"])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

response_template = """<!doctype html>
  <head>
    <title>QR URL redirect</title>
  </head>
  <body>
{}
  </body>
</html>"""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def lookupQR():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = UPLOAD_WEB_ACCESS + filename
            soup = Soup(requests.get("http://zxing.org/w/decode", params={'u': url}).text)
            if "Parsed Result TypeURI" in soup.find('body').text:
                return redirect(soup.findAll('pre')[-1].text)
            elif "Parsed Result Type" in soup.find('body').text:
                return redirect("http://zxing.org/w/decode?u=" + quote_plus(url))
            return response_template.format("Couldn't parse QR code :(")
        return response_template.format("Invalid file :(")
    return response_template.format("""    <h3>Upload file</h3>
    <form action="" method="POST" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>""")

app.run(host='0.0.0.0', port=7578, debug=True)


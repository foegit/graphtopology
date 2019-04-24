import os
from jinja2 import evalcontextfilter
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from werkzeug.utils import secure_filename
import shortuuid

from topo import Topology


UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.template_filter()
def fnum(value):
    value = round(value, 2)
    if int(value) == value:
      value = int(value)
    return value

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/topology", methods=["POST"])
def topology():
  if 'file' not in request.files:
    flash('No file part')
    return redirect(request.url)
  file = request.files['file']
  filename = file.filename
  if filename == '':
    flash('No selected file')
    return redirect(request.url)
  ext = os.path.splitext(filename)[1][1:]
  topology = Topology(file=file.stream, type=ext)
  return render_template('topology.html', t=topology.make_report())

if __name__ == "__main__":
  app.run()

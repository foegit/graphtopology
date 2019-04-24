import os
from flask import Flask, flash, redirect, render_template, request, url_for

from topo import Topology

ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

app = Flask(__name__)

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

@app.route('/about')
def about():
  return render_template('about.html')
@app.route("/topology", methods=['GET', 'POST'])
def topology():
  if 'file' not in request.files:
    flash('Потрібно вибрати файл', category='error')
    return redirect(url_for('index'))
  file = request.files['file']
  filename = file.filename
  if filename == '':
    flash('Файл не вибрано', category='error')
    return redirect(url_for('index'))
  ext = os.path.splitext(filename)[1][1:]
  if not allowed_file(filename):
    flash('Формат {} не підтримується'.format(ext), category='error')
    return redirect(url_for('index'))
  topology = Topology(file=file.stream, type=ext)
  return render_template('topology.html', t=topology.make_report())

app.secret_key = 'fpaiajfbasshougiubfajs'
if __name__ == "__main__":
  app.run()

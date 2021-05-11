from flask import Flask, render_template, flash, request
from imageupload import main
app = Flask(__name__)

app.secret_key = 'd0a630b1636b428598c8fc860ec3c314'
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  main()
  flash("It worked!")
  return render_template('index.html')


if __name__ == '__main__':
  app.run(debug=True)

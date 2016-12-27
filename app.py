from flask import Flask
from flask import render_template
from flask import request
application = Flask(__name__)

@application.route("/")
def app():
    return render_template("app.html")

@application.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

if __name__ == "__main__":
    application.run(host='0.0.0.0')

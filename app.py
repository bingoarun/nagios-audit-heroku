from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import make_response
import os
import time



application = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
OUTPUT_FOLDER = 'output/'

@application.route("/")
def app():
    return render_template("app.html")

@application.route('/upload',methods = ['POST', 'GET'])
def upload():
   if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        timestr = time.strftime("%Y%m%d%H%M%S")
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            tmp_filename = file.filename + timestr
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], tmp_filename))
            cmd_str = ("nagios-audit --input_file=%s%s --output_file=%s%s" % (UPLOAD_FOLDER,tmp_filename,OUTPUT_FOLDER,tmp_filename))
            print cmd_str
            os.system(cmd_str)
            output_str = open((OUTPUT_FOLDER+tmp_filename)).read()
            response = make_response(output_str)
            response.headers["Content-Disposition"] = "attachment; filename=test.csv"
            return response
            #return redirect(url_for('result',filename=(UPLOAD_FOLDER+tmp_filename)))
            #return render_template("result.html",filename=(OUTPUT_FOLDER+tmp_filename))
        return None

    

application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if __name__ == "__main__":
    application.run(host='0.0.0.0')

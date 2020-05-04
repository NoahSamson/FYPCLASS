# imports
from flask import Flask, render_template, request
from flaskwebgui import FlaskUI

import os
import shutil
import json

from imageholder import ImageHolder
import predictionmodel

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# ui = FlaskUI(app)

class Server:

    def __init__(self):
        # methods = ['POST']
        self.source_path = './static/uploads/source/'
        self.detection_path = './static/uploads/detections/'
        self.rmodel = predictionmodel.PredictionModel('retinanetresnet101', predictionmodel.RETINANET_MODEL_PATH)
        self.rmodel.model_load()
        print('loaded Models')

    def index_page(self):
        return render_template('home.html')

    def delete_static_images(self):
        all_files = ''
        for root, dirs, files in os.walk(self.detection_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print('File %s could not be deleted. Reason: %s' % (file, e))
        for root, dirs, files in os.walk(self.source_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print('File %s could not be deleted. Reason: %s' % (file, e))
        return render_template('home.html')

    def predict_image(self):

        data = request.get_json()
        simg = ImageHolder('source', data['file_name'],self.source_path, None, data['image_data'])

        # simg = ImageHolder('source', self.source_path, None, request.json)

        result = self.rmodel.get_prediction_results(simg)
        r = json.dumps(result)
        r = json.loads(r)

        return render_template('result.html', preds = r)


server = Server()
app.add_url_rule('/', 'index', lambda: server.index_page())
app.add_url_rule('/delete_files', 'delete_files', lambda: server.delete_static_images())
# app.add_url_rule('/predict_image', 'predict_image', server.predict_image())
app.add_url_rule('/predict_image', 'predict_image', lambda: server.predict_image(), methods=['GET', 'POST'])


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    return response


if __name__ == '__main__':
    # ui.run(host='0.0.0.0', port=5000, debug=False)
    # ui.run()
    # app.run()
    FlaskUI(app).run()

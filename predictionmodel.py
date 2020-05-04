#imports
from keras_retinanet import models as m
from PIL import Image
import pandas
import cv2
import time

# imports for Retinanet
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# Model paths
RETINANET_MODEL_PATH = 'model/Copy of resnet101_csv_40.h5'
THRESHOLD_SCORE = 0.6
CLASSES_FILE = 'static/csv/RetinanetZWGClass.csv'


class PredictionModel:
    def __init__(self, model_type, model_path):
        self.model_type = model_type
        self.model_path = model_path
        self.model = None
        self.labelstonames = None

    # Load Model
    def model_load(self):
        if self.model_type == 'retinanetresnet101':
            self.model = m.load_model(self.model_path, backbone_name='resnet101')
            self.model = m.convert_model(self.model)
            self.labelstonames = pandas.read_csv(CLASSES_FILE, header=None).T.loc[0].to_dict()

    # Get prediction Results
    def get_prediction_results (self, simg):
        simg.base64_to_pil()

        # save image and update path
        source_save = Image.open(simg.imgpil)
        simg.imgpath = simg.imgpath + simg.imgname + '.jpg'
        source_save.save(simg.imgpath)
        predictions = self.model_predict(simg)

        return predictions

    # Object Detection
    def model_predict(self, simg):
        img = read_image_bgr(simg.imgpil)
        timg = img.copy()
        drawimg = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)

        # preprocess
        img = preprocess_image(img)

        # Json for predictions
        data = {"source": simg.imgpath}

        # cropped images
        cimg = []

        # process image
        start = time.time()
        boxes, scores, labels = self.model.predict_on_batch(pandas.np.expand_dims(img, axis=0))

        # count animals

        count = 0
        zebra_count = 0
        wildebeest_count = 0
        gazelle_count = 0

        # Visualize Detections
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            # scores are sorted
            if score < THRESHOLD_SCORE:
                break
            lcolor = label_color(label)

            b = box.astype(int)
            draw_box(drawimg, b, color=lcolor)

            #crop image
            cropped = timg[b[1]:b[3], b[0]:b[2]]
            # Get the correct label and save
            # Get the correct label
            if label == 0:
                animal = 'wildebeest'
                wildebeest_count = wildebeest_count + 1
                cfilename = './static/uploads/detections/wildebeest/' + simg.imgname + animal + str(count) + '.jpg'
                cv2.imwrite(cfilename, cropped)
            elif label == 1:
                animal = 'zebra'
                zebra_count = zebra_count + 1
                cfilename = './static/uploads/detections/zebra/' + simg.imgname + animal + str(count) + '.jpg'
                cv2.imwrite(cfilename, cropped)
            elif label == 2:
                animal = 'gazelleThomsons'
                gazelle_count = gazelle_count + 1
                cfilename = './static/uploads/detections/gazelleThomsons/' + simg.imgname + animal + str(count) + '.jpg'
                cv2.imwrite(cfilename, cropped)
            else:
                animal = label
                cfilename = './static/uploads/detections/' + simg.imgname + animal + str(count) + '.jpg'
                cv2.imwrite(cfilename, cropped)

            count = count + 1

            caption = "{} {:.3f}".format(self.labelstonames[label], score)
            draw_caption(drawimg, b, caption)

            # create list of detected animals
            cimg.append({
                "img_src": cfilename,
                "label": animal
            })

        data["wcount"] = wildebeest_count
        data["zcount"] = zebra_count
        data["gcount"] = gazelle_count
        data["prediction"] = cimg
        print(data)
        detected_img = Image.fromarray(drawimg.astype('uint8'), 'RGB')
        detected_img.save("./static/uploads/source/" + simg.imgname +"detected.jpg")
        data["detected"] = './static/uploads/source/' + simg.imgname +'detected.jpg'
        return data



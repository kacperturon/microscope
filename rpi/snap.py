import cv2
import boto3
import os
import logging
import time
from zoneinfo import ZoneInfo
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from picamera2 import Picamera2

logging.basicConfig(filename='snap.log', level=20)
# logging.[debug | info | warning]

VERSION = "0.01.00"
ENVIRONMENT = os.getenv('SNAP_ENV') or 'dev'
TIME_ZONE = "Europe/Warsaw"

BUCKET_S3 = ""
BUCKET_S3_PROD = 'microscope-grain'
BUCKET_S3_DEV = 'microscope-grain-dev'
PICTURES_TEMP_FOLDER = 'temp'
PICTURES_FOLDER = 'pictures'

S3 = boto3.resource('s3')
CLIENT_S3 = boto3.client('s3', region_name='eu-central-1')

CAM_PORT = os.getenv('SNAP_CAM_PORT') or 1
PI_CAM_ENABLED = False
PI_CAM = None

# PI_CAM.controls.ExposureTime = 10000
# PI_CAM.controls.AnalogueGain = 1.0


def create_app():
    app = Flask(__name__)
    CORS(app)

    CAM = cv2.VideoCapture(CAM_PORT)
    time.sleep(0.5)
    CAM.read()

    @app.route('/env')
    def environment():
        return ENVIRONMENT

    @app.route("/ping")
    def ping_pong():
        return "pong"

    @app.route("/pic")
    def upload_pic_S3():
        (image_name, file_location) = take_pic()
        if image_name is None:
            return "", 500
        url = upload_file_S3(file_location, image_name, BUCKET_S3)
        if url is None:
            return "", 500
        return jsonify(
            id=image_name,
            url=url
        )

    @app.route("/pic/<pic_id>/delete")
    def delete_pic_S3(pic_id):
        copy_source = {
            'Bucket': BUCKET_S3,
            'Key': f"{PICTURES_TEMP_FOLDER}/{pic_id}"
        }
        deleted = S3.meta.client.delete_object(
            Bucket=copy_source["Bucket"], Key=copy_source["Key"])
        logging.warning(deleted)
        return "", 200

    @app.route("/pic/<pic_id>/move")
    def move_pic_S3(pic_id):
        copy_source = {
            'Bucket': BUCKET_S3,
            'Key': f"{PICTURES_TEMP_FOLDER}/{pic_id}"
        }
        try:
            S3.meta.client.copy(copy_source, BUCKET_S3,
                                f"{PICTURES_FOLDER}/{pic_id}")
            S3.meta.client.delete_object(
                Bucket=copy_source["Bucket"], Key=copy_source["Key"])
        except Exception as e:
            logging.warning(e)
            logging.warning(
                f"Could not copy file from: {copy_source} to: {PICTURES_FOLDER}/{pic_id} or delete {copy_source['Key']}")
            return "", 500
        return "", 200

    return app


def take_pic(pictures_folder=PICTURES_FOLDER):
    image = None
    if PI_CAM_ENABLED is True:
        PI_CAM.start()
        time.sleep(1)
        image = PI_CAM.capture_array()
        PI_CAM.stop()
    else:
        CAM = cv2.VideoCapture(CAM_PORT)
        time.sleep(1)
        _, image = CAM.read()
        # unload CAM so the microscope display can access data
        CAM.release()
        CAM = None
    if image is not None:
        time_str = datetime.now(ZoneInfo(TIME_ZONE)).strftime('%Y%m%d-%H%M%S')
        image_name = f"{time_str}.jpg"
        file_location = f"./{pictures_folder}/{image_name}"
        saved = cv2.imwrite(file_location, image)
        if not saved:
            logging.warning(f"Could not save file: {file_location}")
            return (None, None)
        else:
            return (image_name, file_location)
    else:
        logging.warning(
            f"Could not take an image with device with device_id: {CAM_PORT}")


def upload_file_S3(file_location, filename, bucket=BUCKET_S3):
    try:
        CLIENT_S3.upload_file(
            file_location, bucket, f"{PICTURES_TEMP_FOLDER}/{filename}")
    except:
        logging.warning(
            f"Could not upload file to S3: {PICTURES_TEMP_FOLDER}/{filename} bucket: {bucket} from {file_location}")
        return None
    return f"https://{BUCKET_S3}.s3.eu-central-1.amazonaws.com/{PICTURES_TEMP_FOLDER}/{filename}"


def camera_indices():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr


if __name__ == 'snap':
    if ENVIRONMENT == 'prod':
        BUCKET_S3 = BUCKET_S3_PROD
    else:
        BUCKET_S3 = BUCKET_S3_DEV
    if PI_CAM_ENABLED:
        PI_CAM = Picamera2()
        PI_CAM.create_still_configuration()
    logging.info('--------------------------------------------')
    logging.info('Server started')
    logging.info(f'Environment: {ENVIRONMENT}')
    logging.info(f'Version: {VERSION}')
    logging.info(f"Available cameras: {camera_indices()}")
    logging.info(f"PI cam enabled: {PI_CAM_ENABLED}")
    logging.info(f"Camera port used: {CAM_PORT}")
    logging.info(f"Bucket set to: {BUCKET_S3}")
    app = create_app()

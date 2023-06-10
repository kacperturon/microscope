import boto3
import cv2
import time
from flask import Flask, jsonify
from flask_cors import CORS
import logging

logging.basicConfig(filename='snap.log', level=20)
# logging.[debug | info | warning]

CAM_PORT = 0
CLIENT_S3 = boto3.client('s3', region_name='eu-central-1')
BUCKET_S3 = 'microscope-grain'
PICTURES_TEMP_FOLDER = 'temp'
PICTURES_FOLDER = 'pictures'
BUCKET_ROOT_URL_S3 = 'https://microscope-grain.s3.eu-central-1.amazonaws.com'
S3 = boto3.resource('s3')


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/ping")
    def ping_pong():
        return "pong"

    @app.route("/pic")
    def upload_pic_S3():
        (image_name, file_location) = take_pic()
        if image_name is None:
            return 500
        url = upload_file_S3(file_location, image_name)
        if url is None:
            return 500
        return jsonify(
            id=image_name,
            url=url
        )

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
        except:
            logging.warning(
                f"Could not copy file from: {copy_source} to: {PICTURES_FOLDER}/{pic_id} or delete {copy_source['Key']}")
            return 500
        return 200

    return app


def take_pic(pictures_folder=PICTURES_FOLDER):
    CAM = cv2.VideoCapture(CAM_PORT)
    result, image = CAM.read()
    # unload CAM so the microscope display can access data
    CAM = None
    if result:
        time_str = time.strftime("%Y%m%d-%H%M%S")
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

    return f"{BUCKET_ROOT_URL_S3}/{PICTURES_TEMP_FOLDER}/{filename}"


create_app()

import boto3
import cv2
import time
from flask import Flask, jsonify
from flask_cors import CORS
import json
import socket
from urllib.request import urlopen


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

    @app.route("/upload/logs")
    def upload_logs_S3():
        pass

    @app.route("/pic")
    def upload_pic_S3():
        (image_name, file_location) = take_pic()
        url = upload_file_S3(file_location, image_name)
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
        S3.meta.client.copy(copy_source, BUCKET_S3,
                            f"{PICTURES_FOLDER}/{pic_id}")
        S3.meta.client.delete_object(
            Bucket=copy_source["Bucket"], Key=copy_source["Key"])
        return "ok"

    return app


def internet_on():
    try:
        response = urlopen('https://www.google.com/', timeout=10)
        return True
    except:
        return False


def update_config_S3():
    s3object = S3.Object(BUCKET_S3, 'config.json')

    data = {
        "server_local_ip": socket.gethostbyname(socket.getfqdn())
    }

    s3object.put(
        Body=(bytes(json.dumps(data).encode('UTF-8')))
    )


def take_pic(pictures_folder=PICTURES_FOLDER):
    CAM = cv2.VideoCapture(CAM_PORT)
    result, image = CAM.read()
    CAM = None
    if result:
        time_str = time.strftime("%Y%m%d-%H%M%S")
        image_name = f"{time_str}.jpg"
        file_location = f"./{PICTURES_FOLDER}/{image_name}"
        saved = cv2.imwrite(file_location, image)
        if not saved:
            print("could not save")
            # TODO: add logging here
            pass
        else:
            return (image_name, file_location)
    else:
        # TODO: add logging here
        pass


def upload_file_S3(file_location, filename, bucket=BUCKET_S3):
    print(file_location)
    print(filename)
    uploaded = CLIENT_S3.upload_file(
        file_location, bucket, f"{PICTURES_TEMP_FOLDER}/{filename}")
    # client.upload_file('images/image_0.jpg', 'mybucket', 'image_0.jpg')

    # if not uploaded:
    #     print('could not upload')
    #     # TODO: add logging here
    #     pass
    # else:
    return f"{BUCKET_ROOT_URL_S3}/{PICTURES_TEMP_FOLDER}/{filename}"


create_app()

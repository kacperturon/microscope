import boto3
import cv2
import time
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CAM_PORT = 0
CAM = cv2.VideoCapture(CAM_PORT)
CLIENT_S3 = boto3.client('s3', region_name='eu-central-1')
BUCKET_S3 = 'microscope-grain'
PICTURES_FOLDER = 'pictures'
BUCKET_ROOT_URL_S3 = 'https://microscope-grain.s3.eu-central-1.amazonaws.com'


@app.route("/ping")
def ping_pong() -> str:
    return "pong"


@app.route("/upload/logs")
def upload_logs_S3():
    pass


@app.route("/upload/pic")
def upload_pic_S3() -> str:
    (image_name, file_location) = take_pic()
    url = upload_file_S3(file_location, image_name)
    return url


def take_pic(pictures_folder=PICTURES_FOLDER) -> tuple[str, str] | None:
    result, image = CAM.read()
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


def upload_file_S3(file_location, filename, bucket=BUCKET_S3) -> None:
    print(file_location)
    print(filename)
    uploaded = CLIENT_S3.upload_file(
        file_location, bucket, f"{PICTURES_FOLDER}/{filename}")
    # client.upload_file('images/image_0.jpg', 'mybucket', 'image_0.jpg')

    # if not uploaded:
    #     print('could not upload')
    #     # TODO: add logging here
    #     pass
    # else:
    return f"{BUCKET_ROOT_URL_S3}/{PICTURES_FOLDER}/{filename}"

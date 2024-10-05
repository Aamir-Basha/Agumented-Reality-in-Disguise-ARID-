# This file is for show casing the project without the Monocle


import cv2
import numpy as np
import io
import PIL.Image as Image
from qreader import QReader
import os

async def detect_monocle(n):
    image = cv2.imread(f'output{n}.jpg')
    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecode(image)

    if data:
        return data
    else:
        return ("no data found")
     

async def detect_monocle_GS(n):
    image_path = f'output/output{n}.jpg'
    image = cv2.imread(image_path, 0)

    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return "no data found"

    cv2.imwrite(f'output/cv2gs{n + 1}.jpg', image)

    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecode(image)

    if data[0]:
        return data[0]
    else:
        return "no data found"


async def print_tharashholding(n):
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(f'output/output{n}.jpg'), cv2.COLOR_BGR2RGB)
    imgJPG = cv2.imread(f'output/output{n}.jpg', 0)

    if image is None or imgJPG is None:
        print(f"Error: Unable to load image at output/output{n}.jpg")
        return

    thresholds = [200, 150, 120, 80, 50]
    threshold_images = []

    for threshold_value in thresholds:
        ret, thresh = cv2.threshold(imgJPG, threshold_value, 255, cv2.THRESH_BINARY)
        threshold_images.append(thresh)
        cv2.imwrite(f'output/thresh_bi_{threshold_value}_{n}.jpg', thresh)

    for i, thresh in enumerate(threshold_images):
        data = qreader.detect_and_decode(image=thresh)
        print(f"Threshold {thresholds[i]}: ", data)
        

async def detect_qreader_monocle(n):
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(f'output/output{n}.jpg'), cv2.COLOR_BGR2RGB)
    imgJPG = cv2.imread(f'output/output{n}.jpg', 0)

    if image is None or imgJPG is None:
        print(f"Error: Unable to load image at output/output{n}.jpg")
        return

    decoded_text = qreader.detect_and_decode(image=image)
    if decoded_text:
        return decoded_text

    thresholds = [200, 150, 120, 80, 50]
    threshold_images = []

    for threshold_value in thresholds:
        ret, thresh = cv2.threshold(imgJPG, threshold_value, 255, cv2.THRESH_BINARY)
        threshold_images.append(thresh)
        cv2.imwrite(f'output/thresh_bi_{threshold_value}_{n}.jpg', thresh)

    if decoded_text and decoded_text[0] is not None:
        return decoded_text

    for i, thresh in enumerate(threshold_images):
        data = qreader.detect_and_decode(image=thresh)
        print(data, f"Threshold {thresholds[i]}")
        
        if data and data[0] is not None:
            return data

    print("No QR Code found in the image.")
    return None


async def detect_laptop_test(i):
    try:
        file_path = f'qr_samples/sample_image{i}.jpg'

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                qr_code = f.read()

                if qr_code:
                    print(f"QR code detected in {file_path}")
                    return qr_code
                else:
                    print(f"No QR code found in {file_path}")
        else:
            print(f"File {file_path} does not exist")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")


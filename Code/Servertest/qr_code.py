import cv2
import numpy as np
import io
import PIL.Image as Image



async def detect_monocle(n):
    #for n in range(100):
        image = cv2.imread(f'output{n}.jpg')
        detector = cv2.QRCodeDetector()
        data, vertices_array, _ = detector.detectAndDecode(image)
        
        if data:
            print(data)
            return data
        else:
            print("No QR Code found in the image.")
            return ("no data found")


## This Function is only for testing the script without the Monocle !!
async def detect_laptop_test():
    try:
        with open('sample_image.jpg', 'rb') as f:
            qr_code = f.read()

        image = Image.open(io.BytesIO(qr_code))  # Open the img in in bytes format
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Convert it to BGR 
        detector = cv2.QRCodeDetector()
        data, vertices_array, _ = detector.detectAndDecode(image)   # Detect the QR-Code data (This will be ASCII)

        if data:
            # Have to change print to -> display() to get it on the Monocle!!
            return data
        else:
            # Have to change print to -> display() to get it on the Monocle!!
            print("No QR Code found in the image.")
            return None
    except FileNotFoundError:
        print("Error: Image file 'sample_image.jpg' not found.")
        return None
    except Exception as e:
        print(f"Error reading image or detecting QR code: {e}")
        return None


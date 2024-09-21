# this file is for testing functions of cv2 and pil to enhance qr code detection

import cv2
import numpy as np
import io
import PIL.Image as Image

async def detect_monocle(n):
    image = cv2.imread(f'output\\output{n}.jpg')
    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecode(image)
    
    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()

    if data:
        return data
    else:
        print("No QR Code found in the image.")
        return ("no data found")
     

async def detect_monocle_GS(n):
    image = cv2.imread(f'output\\output{n}.jpg',0) # 0 = greyscale
    cv2.imwrite(f'output\\cv2gs{n+1}.jpg', image)
    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecode(image)

    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()

    if data:
        return data
    else:
        print("No QR Code found in the image.")
        return ("no data found")
    
async def detect_monocle_thresholding_bi(n):
    image = cv2.imread(f'output\\output{n}.jpg', 0) #greyscale required für thresholding
    detector = cv2.QRCodeDetector()
    # looping thru various thresholds == lighting conditions in main via second argument for ret
    # for i in range(3):
    #    threshold_value = 180 - 40 * i 
    ret, thresh0 = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)
    ret1, thresh1 = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)
    ret2, thresh2 = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
    ret3, thresh3 = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'output\\thresh_bi_{ret}_{n}.jpg', thresh0)
    cv2.imwrite(f'output\\thresh_bi_{ret1}_{n}.jpg', thresh1)
    cv2.imwrite(f'output\\thresh_bi_{ret2}_{n}.jpg', thresh2)
    cv2.imwrite(f'output\\thresh_bi_{ret3}_{n}.jpg', thresh3)
    data = detector.detectAndDecode(thresh1)

    # De-allocate any associated memory usage   
    if cv2.waitKey(0) & 0xff == 27:  
        cv2.destroyAllWindows()

    if data:
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


from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import cv2
import PIL
from PIL import Image
import numpy as np
from io import BytesIO
import tensorflow as tf
import easyocr
import io
import logging
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_SHAPE = (224, 224)
ORIGINAL_IMAGE_PATH = "original_image.png"
NORMALIZED_IMAGE_PATH = "normalized_image.png"
ROI_IMAGE_PATH = "roi_image.png"

logging.basicConfig(level=logging.INFO)

def load_model(model_path):
    """
    Load the TensorFlow model from the specified path.

    Args:
        model_path (str): The path to the saved model.

    Returns:
        tf.keras.Model: Loaded TensorFlow model.
    """
    return tf.keras.models.load_model(model_path)

model_path = r'C:\Users\T480\Desktop\anpr\anpr_model.h5'
model = load_model(model_path)

def read_image(image_encoded):
    """
    Read and decode the uploaded image.

    Args:
        image_encoded (bytes): Encoded image data.

    Returns:
        PIL.Image.Image: Decoded PIL Image.
    """
    try:
        pil_image = Image.open(BytesIO(image_encoded))
        return pil_image
    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
        raise HTTPException(status_code=404, detail="File not found")
    except (PIL.UnidentifiedImageError, cv2.error) as e:
        logging.error(f"Error reading image: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid image format")


def process_image_pil(pil_image):
    """
    Process the PIL image for object detection.

    Args:
        pil_image (PIL.Image.Image): Input PIL image.

    Returns:
        tuple: Tuple containing unchanged image and normalized image.
    """
    try:
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        input_image = np.array(pil_image)

        unchanged_image = np.copy(input_image)
        unchanged_image = np.array(unchanged_image, dtype=np.uint8)
        unchanged_image = cv2.resize(unchanged_image, IMAGE_SHAPE)
        unchanged_image = cv2.cvtColor(unchanged_image, cv2.COLOR_RGB2BGR)

        image_for_norm = np.copy(input_image)
        image_for_norm = np.array(image_for_norm, dtype=np.uint8)
        image_for_norm = cv2.resize(image_for_norm, IMAGE_SHAPE)
        image_for_norm = cv2.cvtColor(image_for_norm, cv2.COLOR_RGB2BGR)

        norm_image = cv2.normalize(image_for_norm, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

        return unchanged_image, norm_image
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


def object_detection(unchanged_image, norm_image):
    """
    Perform object detection on the normalized image.

    Args:
        unchanged_image (numpy.ndarray): Unchanged image.
        norm_image (numpy.ndarray): Normalized image.

    Returns:
        tuple: Tuple containing the image with bounding box and object coordinates.
    """
    try:
        h, w, d = norm_image.shape
        image = norm_image.reshape(1, 224, 224, 3)
        coords = model.predict(image)

        denorm = np.array([w, w, h, h])
        coords = coords * denorm
        coords = coords.astype(np.int32)

        xmin, xmax, ymin, ymax = coords[0]
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        print(pt1, pt2)
        original_copy_with_bbx = cv2.rectangle(unchanged_image, pt1, pt2, (0, 255, 0), 3)

        return original_copy_with_bbx, coords
    except Exception as e:
        logging.error(f"Error in object detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in object detection: {str(e)}")


def extract_roi(original_image, coords):
    """
    Extract the Region of Interest (ROI) from the original image using provided coordinates.

    Args:
        original_image (numpy.ndarray): Original image.
        coords (numpy.ndarray): Object coordinates.

    Returns:
        numpy.ndarray: Extracted ROI image.
    """
    try:
        xmin, xmax, ymin, ymax = coords[0]
        roi = original_image[ymin:ymax, xmin:xmax]

        return roi
    except Exception as e:
        logging.error(f"Error extracting ROI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting ROI: {str(e)}")


def ocr_text(roi_image):
    """
    Perform Optical Character Recognition (OCR) on the ROI image.

    Args:
        roi_image (numpy.ndarray): ROI image.

    Returns:
        list: List of detected texts.
    """
    try:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(roi_image)

        return [detection[1] for detection in result]
    except Exception as e:
        logging.error(f"Error in OCR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in OCR: {str(e)}")


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predicts object coordinates in the uploaded image.

    Args:
        file (UploadFile): The uploaded image file.

    Returns:
        StreamingResponse: Predicted image with object detection.
    """
    try:
        pil_image = read_image(await file.read())
        original_image, normalized_image = process_image_pil(pil_image)
        
        logging.info(f"Input Image Shape: {original_image.shape}")
        original_copy_with_bbx, coords = object_detection(original_image, normalized_image)

        roi_image = extract_roi(original_copy_with_bbx, coords)

        ocr_result = ocr_text(roi_image)
        print("OCR Result:", ocr_result)

        original_image_base64 = base64.b64encode(cv2.imencode('.png', original_image)[1].tobytes()).decode('utf-8')
        original_copy_with_bbx_base64 = base64.b64encode(cv2.imencode('.png', original_copy_with_bbx)[1].tobytes()).decode('utf-8')
        roi_image_base64 = base64.b64encode(cv2.imencode('.png', roi_image)[1].tobytes()).decode('utf-8')

        return {
            "original_image": original_image_base64,
            "original_copy_with_bbx": original_copy_with_bbx_base64,
            "roi_image": roi_image_base64,
            "ocr_results": ocr_result
        }

    except HTTPException as http_exc:
        raise http_exc 
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import tensorflow as tf
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = r'C:\Users\T480\Desktop\anpr\anpr_model.h5'
model = tf.keras.models.load_model(model_path)

IMAGE_SIZE = (224, 224)

def read_image(image_encoded):
    try:
        pil_image = Image.open(BytesIO(image_encoded))
        return pil_image
    except Exception as e:
        print(f"Error reading image: {str(e)}")
        return None

def process_image_pil(pil_image):
    try:
        # Convert to RGB (if not already in RGB format)
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        _image = np.array(pil_image)
        image = cv2.resize(_image, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV visualization

        print("Original Image Data Type:", image.dtype)
        print("Original Image Shape:", image.shape)
        print("Original Image Min:", np.min(image))
        print("Original Image Max:", np.max(image))
        
        norm_image = cv2.normalize(image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        print("Normalized Image Data Type:", norm_image.dtype)
        print("Normalized Image Shape:", norm_image.shape)
        print("Normalized Image Min:", np.min(norm_image))
        print("Normalized Image Max:", np.max(norm_image))

        cv2.imwrite("original_image.png", cv2.cvtColor(_image, cv2.COLOR_RGB2BGR))
        cv2.imwrite("normalized_image.png", cv2.cvtColor(norm_image, cv2.COLOR_RGB2BGR))
        
        return norm_image
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


def object_detection(norm_image):
    h, w, d = norm_image.shape

    # Make a copy of the image to avoid modifying the original
    image_copy = np.copy(norm_image)
    image = norm_image.reshape(1, 224, 224, 3)

    coords = model.predict(image)

    denorm = np.array([w, w, h, h])
    coords = coords * denorm
    coords = coords.astype(np.int32)

    xmin, xmax, ymin, ymax = coords[0]
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    print(pt1, pt2)
    cv2.rectangle(image_copy, pt1, pt2, (0, 255, 0), 3)

    return image_copy, coords


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        pil_image = read_image(await file.read())
        image = process_image_pil(pil_image)

        print("Input Image Shape:", image.shape)
        result_image, coords = object_detection(image)
        print("Predicted Coords:", coords)

        # Save the result image for debugging
        # cv2.imwrite("result_image_debug.png", cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

        result_image_bytes = cv2.imencode('.png', result_image)[1].tobytes()
        return StreamingResponse(io.BytesIO(result_image_bytes), media_type="image/png")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

from fastapi import FastAPI, File, UploadFile, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
import tensorflow as tf


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = r'C:\Users\HP\Desktop\saved_model\sys_model.h5'
model = tf.keras.models.load_model(model_path)


def read_image(image_encoded):
    try:
        pil_image = Image.open(BytesIO(image_encoded))
        return pil_image
    except Exception:
        return None


def process_image_pil(pil_image):
    try:
        image = pil_image.resize((224, 224))
        image = np.array(image, dtype=np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = image / 255
        image = image.reshape(1, 224, 224, 3)
        return image
    except Exception:
        return None


def object_detection(image):
    h, w, d = image.shape[1:]

    coords = model.predict(image)

    denorm = np.array([w, w, h, h])
    coords = coords * denorm
    coords = coords.astype(np.int32)

    xmin, xmax, ymin, ymax = coords[0]
    pt1 = (xmin, ymin)
    pt2 = (xmax, ymax)
    cv2.rectangle(image[0], pt1, pt2, (0, 255, 0), 3)
    return image[0], coords


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        pil_image = read_image(await file.read())
        if pil_image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")

        image = process_image_pil(pil_image)
        if image is None:
            raise HTTPException(status_code=500, detail="Error processing image")

        result_image, coords = object_detection(image)
        result_image_bytes = cv2.imencode('.png', result_image)[1].tobytes()
        return StreamingResponse(BytesIO(result_image_bytes), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

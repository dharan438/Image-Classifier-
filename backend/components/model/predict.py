from keras.models import load_model
from keras.utils import load_img, img_to_array
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join
import aiofiles
import uuid
import shutil

width, height = 150, 150
model_name = "model.h5"
temp_storage = "temp_storage/"

model = load_model(model_name)
model.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"])


def predict(img):
    img = load_img(img, target_size=(width, height))
    img_arr = img_to_array(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    images = np.vstack([img_arr])
    classes = model.predict(images)
    classes = classes[0][0]

    return "car" if classes == 1 else "bike"

async def handle_image_upload(files):
    cars, bikes = [], []

    pid = str(uuid.uuid4())
    path = f"{temp_storage}/{pid}/"

    mkdir(path)
    print(f"Temporarily storing files in {path}...")

    for file in files:
        async with aiofiles.open(path + file.filename, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
    print("Files stored. Predicting...")

    files = [f for f in listdir(path) if isfile(join(path, f))]
    print(f"Available files: {files}")

    for file in files:
        res = predict(path + file)
        print(f"Predicted {file} to be a {res}")

        cars.append(file) if res == "car" else bikes.append(file)
    
    shutil.rmtree(path)
    print("Removed temporary files.")

    return {
        "car": {"files": cars, "count": len(cars)},
        "bike": {"files": bikes, "count": len(bikes)},
    }

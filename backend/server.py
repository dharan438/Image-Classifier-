import uvicorn
from fastapi import FastAPI, File, UploadFile
from components.model.predict import handle_image_upload
from fastapi.middleware.cors import CORSMiddleware

from typing import List

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/predict")
async def predict_api(files: List[UploadFile], name: str = "John Doe", consent: bool = False):
    results = await handle_image_upload(files)
    if not results:
        return {"error": "An error occurred."}
    return {"results": results}

#todo: cache results
#todo: add model training endpoint
#todo: add model accuracy endpoint

if __name__ == "__main__":
    uvicorn.run(app)

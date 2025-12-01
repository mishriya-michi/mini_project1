from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ransomware Decryptor Backend is running successfully!"}

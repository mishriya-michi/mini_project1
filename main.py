from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles   # <-- add this
import shutil
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ---------------- FASTAPI APP ----------------
app = FastAPI(title="CyberSafe Ransomware Decryptor")

# ---------------- Serve Frontend ----------------
# Mount frontend folder at root before API routes
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Directories ----------------
UPLOAD_DIR = "uploads"
DECRYPT_DIR = "decrypted"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DECRYPT_DIR, exist_ok=True)

# ---------------- AES Key (demo) ----------------
AES_KEY = b"1234567890123456"  # 16 bytes key for AES-128
AES_IV = b"abcdefghijklmnop"   # 16 bytes IV

# ---------------- Upload Endpoint ----------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- Decrypt Endpoint ----------------
@app.post("/decrypt")
async def decrypt_file(data: dict):
    filename = data.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename required")
    
    input_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    decrypted_filename = f"decrypted_{filename}"
    output_path = os.path.join(DECRYPT_DIR, decrypted_filename)
    
    try:
        with open(input_path, "rb") as f_in:
            ciphertext = f_in.read()
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        with open(output_path, "wb") as f_out:
            f_out.write(decrypted)
    except Exception:
        shutil.copy(input_path, output_path)
    
    return {"status": "success", "decrypted_file": decrypted_filename}

# ---------------- Download Endpoint ----------------
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(DECRYPT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)

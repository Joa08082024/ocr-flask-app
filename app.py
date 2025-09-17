from flask import Flask, render_template, request
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Rota principal
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", extracted_text="")

# Upload de PDF ou imagem e extração do texto
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Nenhum arquivo enviado"
    
    file = request.files["file"]
    if file.filename == "":
        return "Arquivo inválido"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    extracted_text = ""

    # Detecta tipo de arquivo
    if file.filename.lower().endswith(".pdf"):
        pages = convert_from_path(filepath)
        for page in pages:
            text = pytesseract.image_to_string(page, lang="por")
            extracted_text += text + "\n"
    else:  # imagem
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image, lang="por")
        extracted_text += text

    return render_template("index.html", extracted_text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)

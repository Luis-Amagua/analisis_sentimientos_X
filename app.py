import pandas as pd
import torch
import emoji
import re
import matplotlib.pyplot as plt
from flask import Flask, jsonify, render_template
from transformers import pipeline
from io import BytesIO
import base64

# Cargar los datos desde el archivo CSV
file_path = "tweets.csv"
df = pd.read_csv(file_path)

# Función de limpieza de texto
def limpiar_texto(texto):
    texto = texto.lower()  # Convertir a minúsculas
    texto = re.sub(r"http\S+|www\S+|https\S+", "", texto, flags=re.MULTILINE)  # Eliminar URLs
    texto = re.sub(r"@\w+|#\w+", "", texto)  # Eliminar menciones y hashtags
    texto = re.sub(r"[^\w\s]", "", texto)  # Eliminar signos de puntuación
    texto = emoji.demojize(texto)  # Convertir emojis a texto
    return texto

# Aplicar limpieza
df["text"] = df["text"].astype(str).apply(limpiar_texto)

# Definir el dispositivo para el modelo
device = 0 if torch.cuda.is_available() else -1  

# Cargar el modelo de análisis de sentimientos
modelo_sentimiento = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment", device=device)

# Función de análisis de sentimiento
def analizar_sentimiento(texto):
    try:
        resultado = modelo_sentimiento(texto[:512])  # Limitar a 512 caracteres
        etiqueta = int(resultado[0]['label'].split()[0])
        if etiqueta > 3:
            return "positivo"
        elif etiqueta < 3:
            return "negativo"
        else:
            return "neutral"
    except Exception as e:
        return "error"

# Aplicar el análisis de sentimiento
df["sentimiento"] = df["text"].apply(analizar_sentimiento)

# Contar sentimientos
positivos = sum(df["sentimiento"] == "positivo")
negativos = sum(df["sentimiento"] == "negativo")
neutrales = sum(df["sentimiento"] == "neutral")
total_tweets = len(df)

# Función para generar gráfico de pastel
def generar_grafico():
    plt.figure(figsize=(6, 6))
    etiquetas = ["Positivo", "Negativo", "Neutral"]
    valores = [positivos, negativos, neutrales]
    colores = ["green", "red", "gray"]
    plt.pie(valores, labels=etiquetas, autopct="%1.1f%%", colors=colores, startangle=140)
    plt.title("Distribución de Sentimientos en Twitter")

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

# Iniciar Flask
app = Flask(__name__)

@app.route("/")
def index():
    grafico_base64 = generar_grafico()
    return render_template("index.html", total=total_tweets, positivos=positivos, negativos=negativos, grafico=grafico_base64)

@app.route("/api")
def api():
    return jsonify({
        "total_tweets": total_tweets,
        "positivos": positivos,
        "negativos": negativos,
        "neutrales": neutrales
    })

if __name__ == "__main__":
    app.run(debug=True)

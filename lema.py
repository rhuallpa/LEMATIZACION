from flask import Flask, render_template, request
import openai
import spacy
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar tu clave de API desde el archivo .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cargar el modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')

# Definir la función para lematizar las palabras clave
def lematizar_palabras(palabras):
    palabras_lematizadas = []
    for palabra in palabras:
        doc = nlp(palabra)
        lemas = [token.lemma_ for token in doc]
        palabras_lematizadas.append(' '.join(lemas))
    return palabras_lematizadas

# Definir la función para generar la historia
def generar_historia_con_gpt(palabras_clave):
    palabras_clave_lematizadas = lematizar_palabras(palabras_clave)
    prompt = f"Crea una historia completa de inicio a fin utilizando las siguientes palabras: {', '.join(palabras_clave_lematizadas)}."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un escritor creativo."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        temperature=0.7,
    )
    
    return response.choices[0].message['content'].strip()

# Inicializar Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    palabras_clave = request.form['palabras_clave'].split(',')
    historia = generar_historia_con_gpt(palabras_clave)
    return render_template('index.html', historia=historia)

if __name__ == "__main__":
    app.run(debug=True)

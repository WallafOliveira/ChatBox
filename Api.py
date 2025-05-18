from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
import re

# Configura a API key do Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")

client = genai.Client(api_key=api_key)

app = Flask(__name__)
CORS(app)

# Verifica se a pergunta é sobre e-commerce
def is_ecommerce_related(pergunta):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Essa pergunta está relacionada ao e-commerce? Responda apenas com 'sim' ou 'não'. Pergunta: {pergunta}"]
        )
        return response.text.strip().lower() == "sim"
    except:
        return False

# Gera uma resposta curta e objetiva
def gerar_resposta_formatada(pergunta):
    prompt = f"""
Responda de forma curta, clara e objetiva, usando marcadores simples.
Pergunta: "{pergunta}"
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return formatar_em_html(response.text)

# Formata a resposta em HTML
def formatar_em_html(texto):
    texto = texto.replace("\n", "<br>")
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)

    # Converte listas com "* " em <ul><li>
    itens = re.findall(r'^\* (.+)$', texto, flags=re.MULTILINE)
    if itens:
        lista = "<ul>" + "".join(f"<li>{item}</li>" for item in itens) + "</ul>"
        texto = re.sub(r'(^\* .+$\n?)+', '', texto, flags=re.MULTILINE)
        texto += lista

    return texto

# Rota principal da API
@app.route('/pergunta', methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados.get("pergunta") if dados else None

    if not pergunta:
        return jsonify({"erro": "Pergunta inválida"}), 400

    if not is_ecommerce_related(pergunta):
        return jsonify({"erro": "A pergunta não está relacionada ao e-commerce."}), 400

    try:
        resposta = gerar_resposta_formatada(pergunta)
        return jsonify({"pergunta": pergunta, "resposta": resposta})
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar a pergunta: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

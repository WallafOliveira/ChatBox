from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
import re
import pandas as pd

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")

client = genai.Client(api_key=api_key)

app = Flask(__name__)
CORS(app)

def is_ecommerce_related(pergunta):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Essa pergunta está relacionada ao e-commerce? Responda apenas com 'sim' ou 'não'. Pergunta: {pergunta}"]
        )
        return response.text.strip().lower() == "sim"
    except:
        return False

def gerar_resposta_formatada(pergunta, dados_planilha=None):
    contexto = ""
    if dados_planilha is not None:
        # Resumo simples para o modelo (exemplo: 5 primeiras linhas)
        resumo = dados_planilha.head(5).to_string(index=False)
        contexto = f"\nAqui estão alguns dados relevantes da planilha:\n{resumo}\n"

    prompt = f"""
Responda de forma curta, clara e objetiva, usando marcadores simples.
Pergunta: "{pergunta}"
{contexto}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return formatar_em_html(response.text)

def formatar_em_html(texto):
    texto = texto.replace("\n", "<br>")
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)

    itens = re.findall(r'^\* (.+)$', texto, flags=re.MULTILINE)
    if itens:
        lista = "<ul>" + "".join(f"<li>{item}</li>" for item in itens) + "</ul>"
        texto = re.sub(r'(^\* .+$\n?)+', '', texto, flags=re.MULTILINE)
        texto += lista

    return texto

@app.route('/pergunta', methods=['POST'])
def pergunta():
    pergunta = request.form.get("pergunta")
    arquivo = request.files.get("anexo")

    if not pergunta:
        return jsonify({"erro": "Pergunta inválida"}), 400

    if not is_ecommerce_related(pergunta):
        return jsonify({"erro": "A pergunta não está relacionada ao e-commerce."}), 400

    if not arquivo:
        return jsonify({"erro": "Arquivo Excel não enviado."}), 400

    try:
        dados_planilha = pd.read_excel(arquivo)
    except Exception as e:
        return jsonify({"erro": f"Erro ao ler o arquivo Excel: {str(e)}"}), 400
    
    dados_clientes = dados_planilha.fillna("").to_dict(orient="records")

    try:
        resposta = gerar_resposta_formatada(pergunta, dados_planilha)
        return jsonify({
            "pergunta": pergunta,
            "resposta": resposta,
            "dados_clientes": dados_clientes
        })
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar a pergunta: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

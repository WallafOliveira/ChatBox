from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
import re
import pandas as pd
from docx import Document
from pathlib import Path

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

def ler_documento(arquivo, nome_arquivo):
    try:
        extensao = Path(nome_arquivo).suffix.lower()
        if extensao == ".csv":
            return pd.read_csv(arquivo)
        elif extensao == ".json":
            return pd.read_json(arquivo)
        elif extensao == ".txt":
            return pd.read_table(arquivo)
        elif extensao in [".xlsx", ".xls", ".xlsm", ".xlsb", ".xltx", ".xltm"]:
            return pd.read_excel(arquivo)
        elif extensao == ".html":
            return pd.read_html(arquivo)[0]
        elif extensao == ".docx":
            doc = Document(arquivo)
            textos = [p.text for p in doc.paragraphs if p.text.strip() != ""]
            return pd.DataFrame({"Texto": textos})
        else:
            raise ValueError("Formato de arquivo não suportado.")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {str(e)}")

def gerar_resposta_formatada(pergunta, dados_planilha=None):
    contexto = ""
    if dados_planilha is not None:
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

    dados = None
    dados_clientes = []

    if arquivo:
        try:
            dados = ler_documento(arquivo, arquivo.filename)
            dados_clientes = dados.fillna("").to_dict(orient="records")
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    try:
        resposta = gerar_resposta_formatada(pergunta, dados)
        resposta_json = {
            "pergunta": pergunta,
            "resposta": resposta,
        }
        if dados_clientes:
            resposta_json["dados_clientes"] = dados_clientes

        return jsonify(resposta_json)

    except Exception as e:
        return jsonify({"erro": f"Erro ao processar a pergunta: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)

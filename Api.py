from flask import Flask, request, jsonify
import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")

client = genai.Client(api_key=api_key)

app = Flask(__name__)

# Função para verificar se a pergunta está relacionada ao e-commerce
def is_ecommerce_related(pergunta):
    """Classifica se a pergunta está relacionada ao e-commerce usando a IA"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"Essa pergunta está relacionada ao e-commerce? Responda apenas com 'sim' ou 'não'. Pergunta: {pergunta}"]
        )
        classificacao = response.text.strip().lower()
        return classificacao == "sim"
    except Exception as e:
        return False  # Em caso de erro, assume que não é relacionada

@app.route('/pergunta', methods=['POST'])
def pergunta():
    dados = request.get_json()

    if dados and "pergunta" in dados:
        pergunta = dados["pergunta"]

        if not is_ecommerce_related(pergunta):
            return jsonify({"erro": "A pergunta não está relacionada ao e-commerce."}), 400  # Requisição inválida
        
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[pergunta]
            )
            resposta_gemini = response.text

            return jsonify({"pergunta": pergunta, "resposta": resposta_gemini})
        
        except Exception as e:
            return jsonify({"erro": f"Erro ao processar a pergunta com Gemini: {str(e)}"}), 500  # Erro interno do servidor
    else:
        return jsonify({"erro": "Pergunta inválida"}), 400  # Requisição inválida

if __name__ == '__main__':
    app.run(debug=True)

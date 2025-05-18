# 📦 API Gemini E-commerce — Flask

Esta é uma API desenvolvida em Python utilizando Flask, que usa o modelo Gemini para responder perguntas relacionadas ao e-commerce de forma curta, clara e formatada para fácil leitura no frontend.

---

## 🚀 Tecnologias utilizadas

- Python 3
- Flask
- Flask-CORS
- Google Generative AI (`google.genai`)
- RegEx (para formatação da resposta)

---

## 📂 Estrutura

```
backend/
├── api.py               # Arquivo principal da API
└── requirements.txt     # Dependências (opcional)
```

---

## ⚙️ Configuração

### 1. Clone o projeto:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd backend
```

### 2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências:

```bash
pip install flask flask-cors google-generativeai
```

> Ou, se você tiver um `requirements.txt`, use:
>
> ```bash
> pip install -r requirements.txt
> ```

### 4. Defina sua chave da API Gemini:

Você pode definir via variável de ambiente:

```bash
export GEMINI_API_KEY="sua-chave-aqui"      # Linux/macOS
set GEMINI_API_KEY="sua-chave-aqui"         # Windows
```

---

## ▶️ Executando a API

Com tudo configurado, basta rodar:

```bash
python api.py
```

A API será executada por padrão em: `http://localhost:5000`

---

## 📫 Endpoints

### `POST /pergunta`

Recebe uma pergunta e retorna uma resposta curta e clara se estiver relacionada ao e-commerce.

**Request:**

```json
{
  "pergunta": "Como melhorar o SEO da minha loja virtual?"
}
```

**Response:**

```json
{
  "pergunta": "Como melhorar o SEO da minha loja virtual?",
  "resposta": "<ul><li>Otimize títulos e descrições.</li><li>Use palavras-chave relevantes.</li><li>Mantenha o site rápido e responsivo.</li></ul>"
}
```

> ⚠️ Se a pergunta não for relacionada ao e-commerce, a API retornará:
>
> ```json
> {
>   "erro": "A pergunta não está relacionada ao e-commerce."
> }
> ```

---

## 💡 Funcionalidades

- ✅ Classificação da pergunta (se é sobre e-commerce)
- ✅ Respostas formatadas em HTML com marcadores
- ✅ Respostas curtas, simples e diretas
- ✅ Integração fácil com frontend em React

---

## 📄 Licença

MIT — sinta-se livre para usar e modificar este projeto.
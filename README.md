
# 📦 API Gemini E-commerce — Flask

API desenvolvida em Python utilizando Flask, que utiliza o modelo Gemini (Google Generative AI) para responder perguntas relacionadas a e-commerce de forma curta, clara e formatada em HTML para fácil exibição no frontend.

---

## 🚀 Tecnologias Utilizadas

- Python 3
- Flask
- Flask-CORS
- Google Generative AI (`google.genai`)
- pandas
- python-docx
- RegEx para formatação da resposta em HTML

---

## 📂 Estrutura do Projeto

```
backend/
├── api.py               # Arquivo principal da API Flask
└── requirements.txt     # Dependências do projeto
```

---

## ⚙️ Configuração

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd backend
```

### 2. (Opcional) Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências:

```bash
pip install flask flask-cors google-generativeai pandas python-docx
```

> Ou, se usar um `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure a variável de ambiente da API Gemini:

No Linux/macOS:

```bash
export GEMINI_API_KEY="sua-chave-aqui"
```

No Windows (PowerShell):

```powershell
 GEMINI_API_KEY "sua-chave-aqui"
```

Após definir, reinicie seu terminal para a variável ser reconhecida.

---

## ▶️ Como Executar a API

No terminal, dentro da pasta do projeto:

```bash
python api.py
```

A API estará disponível por padrão em:

```
http://localhost:5000
```

---

## 📫 Endpoints

### POST `/pergunta`

Recebe uma pergunta e, opcionalmente, um arquivo (planilha, documento, etc), e retorna uma resposta curta, clara e formatada, se a pergunta estiver relacionada ao e-commerce.

#### Requisição

- Parâmetros do formulário:
  - `pergunta` (string) — Pergunta do usuário (obrigatório)
  - `anexo` (arquivo) — Arquivo anexado (opcional). Aceita formatos: `.csv`, `.json`, `.txt`, `.xls`, `.xlsx`, `.html`, `.docx`

#### Resposta (JSON)

- Sucesso (200):

```json
{
  "pergunta": "Como melhorar o SEO da minha loja virtual?",
  "resposta": "<ul><li>Otimize títulos e descrições.</li><li>Use palavras-chave relevantes.</li><li>Mantenha o site rápido e responsivo.</li></ul>",
  "dados_clientes": [  // Opcional, se arquivo enviado e com dados
    {
      "Nome": "Cliente 1",
      "Email": "cliente1@email.com",
      ...
    },
    ...
  ]
}
```

- Erro (400 ou 500):

```json
{
  "erro": "Mensagem de erro descritiva."
}
```

---

## 💡 Funcionalidades

- ✅ Verifica se a pergunta é relacionada a e-commerce usando modelo Gemini
- ✅ Lê arquivos anexados em vários formatos populares e extrai dados tabulares
- ✅ Gera respostas curtas, claras e formatadas em HTML usando marcadores
- ✅ Suporta envio e retorno dos dados da planilha para uso no frontend
- ✅ Fácil integração com frontend (exemplo React)

---

## 📦 Dependências

As versões testadas e recomendadas são:

```
Flask==3.1.1
flask_cors==6.0.0
pandas==2.2.3
protobuf==6.31.0
python-docx==1.1.2
google-generativeai
```


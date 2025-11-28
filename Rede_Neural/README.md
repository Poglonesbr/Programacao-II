# 🧠 Sistema de Análise de Sentimentos

Sistema de análise de sentimentos usando **Rede Neural** (TensorFlow/Keras) que classifica textos como **Positivo** ou **Negativo**.

## 📋 Sobre o Projeto

Este projeto utiliza:
- **TensorFlow/Keras**: Rede neural para classificação de sentimentos
- **Flask**: API REST para análise de textos
- **Node.js/Express**: Servidor web e ponte entre frontend e Python
- **Dataset balanceado**: 7.200 reviews (3.600 positivos + 3.600 negativos)

O modelo foi treinado com reviews de aplicativos, removendo avaliações neutras para melhor acurácia.

---

## 🚀 Como Executar

### **Requisitos**
- Python 3.11 (TensorFlow não suporta Python 3.12+)
- Node.js instalado
- Windows PowerShell

### **0️⃣ Configuração Inicial (Apenas na Primeira Vez)**

#### Instalar Python 3.11:
```powershell
winget install --id Python.Python.3.11 -e
```

#### Criar Ambiente Virtual:
```powershell
cd "\Rede_Neural"
python -m venv .venv
```

#### Ativar Ambiente Virtual e Instalar Dependências Python:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### Instalar Dependências Node.js:
```powershell
npm install
```

✅ Pronto! Agora você pode prosseguir para o treinamento do modelo.

---

### **1️⃣ Primeira Execução - Treinar o Modelo**

Abra o PowerShell e execute:

```powershell
cd "\Rede_Neural"
.\.venv\Scripts\Activate.ps1
cd ".\rede neural"
python 3_tf_analise_sentimento.py
```

✅ **Isso irá:**
- Carregar o dataset balanceado (`reviews_balanced.csv`)
- Treinar a rede neural por 30 épocas (~2-5 minutos)
- Salvar o modelo treinado (`modelo_sentimentos.h5`)
- Salvar o tokenizer (`tokenizer.pickle`)
- **Iniciar automaticamente a API Flask na porta 5000**

⚠️ **Mantenha este terminal aberto** - a API Flask precisa estar rodando!

### **2️⃣ Iniciar o Servidor Web**

Em **outro terminal PowerShell**, execute:

```powershell
cd "\Rede_Neural"
npm start
```

✅ Isso iniciará o servidor Node.js na porta 3000

### **3️⃣ Acessar o Sistema**

Abra seu navegador em: **http://localhost:3000**

- Digite uma frase no campo de texto
- Clique em "Analisar Sentimento"
- Veja o resultado: **Positivo** ✅ ou **Negativo** ❌

**Exemplos de teste:**
- "Este produto é excelente!" → Positivo
- "A série é péssima" → Negativo
- "Adorei o atendimento" → Positivo
- "Péssima experiência" → Negativo

---

## 📝 Próximas Execuções

Se você já treinou o modelo e só quer iniciar o sistema:

**Terminal 1 - API Python:**
```powershell
cd "\Rede_Neural"
.\.venv\Scripts\Activate.ps1
cd ".\rede neural"
python api_server.py
```

**Terminal 2 - Frontend:**
```powershell
cd "\Rede_Neural"
npm start
```

---

## 🏗️ Estrutura do Projeto

```
Rede_Neural/
├── public/                    # Frontend (HTML, CSS, JS)
├── rede neural/
│   ├── 3_tf_analise_sentimento.py  # Treina modelo + inicia API
│   ├── api_server.py               # Apenas API (usa modelo existente)
│   ├── analisar.py                 # Script chamado pelo Node.js
│   ├── melhorar_dataset.py         # Cria dataset balanceado
│   ├── modelo_sentimentos.h5       # Modelo treinado
│   ├── tokenizer.pickle            # Tokenizer salvo
│   └── config.pickle               # Configurações
├── reviews.csv                # Dataset original (10.800 reviews)
├── reviews_balanced.csv       # Dataset balanceado (7.200 reviews)
├── server.js                  # Servidor Node.js
├── package.json               # Dependências Node.js
└── requirements.txt           # Dependências Python
```

---

## 🔧 Solução de Problemas

### ❌ "Erro ao processar a requisição"
- Verifique se a API Python está rodando no Terminal 1
- A API deve estar em `http://localhost:5000`

### ❌ "Modelo não encontrado"
- Execute o treinamento primeiro (Passo 1)
- Certifique-se que os arquivos `.h5` e `.pickle` existem em `.\rede neural\`

### 🔄 Retreinar o Modelo
```powershell
cd ".\rede neural"
Remove-Item modelo_sentimentos.h5, tokenizer.pickle, config.pickle
python 3_tf_analise_sentimento.py
```

### 🐍 Python 3.14+ instalado?
TensorFlow requer Python 3.11 ou inferior. Instale Python 3.11:
```powershell
winget install --id Python.Python.3.11 -e
```

---

## 📊 Informações Técnicas

**Modelo:**
- Arquitetura: Embedding → GlobalAveragePooling1D → Dense(24) → Dense(1, sigmoid)
- Vocabulário: 10.000 palavras mais frequentes
- Sequências: 100 tokens (padding='post')
- Épocas: 30
- Acurácia de validação: ~83-85%

**API Endpoints:**
- `POST /analisar` - Analisa sentimento de texto
- `GET /health` - Verifica status da API

---

## 👥 Autores

Henryzzin & Poglones

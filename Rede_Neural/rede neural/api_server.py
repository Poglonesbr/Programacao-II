#!/usr/bin/env python3
"""
API Flask para Análise de Sentimentos
Este script carrega um modelo já treinado e inicia apenas a API.
"""

import os
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, jsonify
from flask_cors import CORS

# Verifica se os arquivos do modelo existem
MODEL_PATH = 'modelo_sentimentos.h5'
TOKENIZER_PATH = 'tokenizer.pickle'
CONFIG_PATH = 'config.pickle'

print("### Verificando arquivos do modelo...")
missing_files = []
if not os.path.exists(MODEL_PATH):
    missing_files.append(MODEL_PATH)
if not os.path.exists(TOKENIZER_PATH):
    missing_files.append(TOKENIZER_PATH)
if not os.path.exists(CONFIG_PATH):
    missing_files.append(CONFIG_PATH)

if missing_files:
    print("\n❌ ERRO: Arquivos não encontrados:")
    for file in missing_files:
        print(f"  - {file}")
    print("\nPor favor, execute primeiro o treinamento:")
    print("  python 3_tf_analise_sentimento.py")
    exit(1)

print("✓ Todos os arquivos encontrados")

# Carrega o modelo
print("\n### Carregando modelo...")
modelo_carregado = tf.keras.models.load_model(MODEL_PATH)
print("✓ Modelo carregado")

# Carrega o tokenizer
print("### Carregando tokenizer...")
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer_carregado = pickle.load(handle)
print("✓ Tokenizer carregado")

# Carrega as configurações
print("### Carregando configurações...")
with open(CONFIG_PATH, 'rb') as handle:
    config_carregado = pickle.load(handle)
print("✓ Configurações carregadas")
print(f"  max_length: {config_carregado['max_length']}")
print(f"  padding_type: {config_carregado['padding_type']}")
print(f"  trunc_type: {config_carregado['trunc_type']}")

# Cria a aplicação Flask
app = Flask(__name__)
CORS(app)

@app.route('/analisar', methods=['POST'])
def analisar_sentimento():
    """Endpoint para analisar sentimento de uma ou mais frases"""
    try:
        data = request.get_json()
        
        # Aceita tanto 'frase' (string única) quanto 'frases' (lista)
        if 'frase' in data:
            frases_avaliacao = [data['frase']]
        elif 'frases' in data:
            frases_avaliacao = data['frases']
        else:
            return jsonify({'erro': 'Envie "frase" ou "frases" no JSON'}), 400
        
        # Processa as frases
        sequencia = tokenizer_carregado.texts_to_sequences(frases_avaliacao)
        padded = pad_sequences(
            sequencia, 
            maxlen=config_carregado['max_length'], 
            padding=config_carregado['padding_type'], 
            truncating=config_carregado['trunc_type']
        )
        
        # Faz predição
        probs = modelo_carregado.predict(padded, verbose=0)
        
        # Prepara resposta
        resultados = []
        for index, frase in enumerate(frases_avaliacao):
            prob_positivo = float(probs[index][0])
            sentimento = 'Positivo' if round(prob_positivo) == 1 else 'Negativo'
            resultados.append({
                'frase': frase,
                'sentimento': sentimento,
                'probabilidade_positivo': prob_positivo,
                'probabilidade_negativo': 1 - prob_positivo
            })
        
        return jsonify({'resultados': resultados})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({'status': 'OK', 'modelo': 'carregado'})

if __name__ == '__main__':
    print("\n=== API Flask iniciada ===")
    print("Endpoints disponíveis:")
    print("  POST /analisar - Analisa sentimento de frase(s)")
    print("  GET  /health   - Verifica status da API")
    print("\nServidor rodando em http://localhost:5000")
    print("Pressione Ctrl+C para parar\n")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

#!/usr/bin/env python3
"""
Script para análise de sentimento - chamado pelo Node.js
Recebe uma frase como argumento e retorna JSON com o resultado
"""
import sys
import json
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Desabilita logs do TensorFlow
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Carrega modelo, tokenizer e config
MODEL_PATH = 'modelo_sentimentos.h5'
TOKENIZER_PATH = 'tokenizer.pickle'
CONFIG_PATH = 'config.pickle'

try:
    # Carrega modelo
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # Carrega tokenizer
    with open(TOKENIZER_PATH, 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    # Carrega configurações
    with open(CONFIG_PATH, 'rb') as handle:
        config = pickle.load(handle)
    
    # Obtém a frase do argumento da linha de comando
    if len(sys.argv) < 2:
        print(json.dumps({'erro': 'Nenhuma frase fornecida'}))
        sys.exit(1)
    
    frase = sys.argv[1]
    
    # Processa a frase
    sequencia = tokenizer.texts_to_sequences([frase])
    padded = pad_sequences(
        sequencia, 
        maxlen=config['max_length'], 
        padding=config['padding_type'], 
        truncating=config['trunc_type']
    )
    
    # Faz predição
    prob = model.predict(padded, verbose=0)
    prob_positivo = float(prob[0][0])
    sentimento = 'Positivo' if round(prob_positivo) == 1 else 'Negativo'
    
    # Retorna resultado como JSON
    resultado = {
        'frase': frase,
        'sentimento': sentimento,
        'probabilidade_positivo': prob_positivo,
        'probabilidade_negativo': 1 - prob_positivo
    }
    
    print(json.dumps(resultado))
    
except Exception as e:
    print(json.dumps({'erro': str(e)}))
    sys.exit(1)

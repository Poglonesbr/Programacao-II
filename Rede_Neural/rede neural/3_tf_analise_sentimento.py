import pandas as pd
import tensorflow as tf
import numpy as np

#configuracoes
vocab_size = 10000
embedding_dim = 64
max_length = 200
trunc_type='pre'
padding_type='pre'
oov_tok = "<OOV>"

print("### Etapa 1 - Carregar dados e organizar")

# carrega arquivo com as avaliacoes (dataset balanceado)
sentimento_df = pd.read_csv("../reviews_balanced.csv")

print(sentimento_df.info())
print(sentimento_df.head())
print(sentimento_df['content'].head())
print(sentimento_df['score'].head())
print(sentimento_df['sentiment'].value_counts())

# O dataset já vem com sentiment (0=Negativo, 1=Positivo)
# Não precisa mais converter pois já está balanceado

# Organiza os dados em Treino e Teste (80% treino, 20% teste)
training_size = int(len(sentimento_df) * 0.8)
training_sentences = sentimento_df['content'].iloc[0:training_size].copy()
testing_sentences = sentimento_df['content'].iloc[training_size:].copy()
print(training_sentences.info())
print(training_sentences.head())

training_labels = sentimento_df['sentiment'].iloc[0:training_size].copy()
testing_labels = sentimento_df['sentiment'].iloc[training_size:].copy()

print("### Etapa 2 - Converter palavras em numeros")
from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index

print("### Etapa 3 - Criar as frases/sequencias")
from tensorflow.keras.preprocessing.sequence import pad_sequences
sequencias_treinamento = tokenizer.texts_to_sequences(training_sentences)
padded_treinamento = pad_sequences(sequencias_treinamento, maxlen=max_length, padding=padding_type, truncating=trunc_type)
sequencias_teste = tokenizer.texts_to_sequences(testing_sentences)
padded_teste = pad_sequences(sequencias_teste, maxlen=max_length, padding=padding_type, truncating=trunc_type)

print("### Etapa 4 - Criando a rede neural")
model = tf.keras.Sequential([
  tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
  # Bidirectional permite ler a frase da esquerda para a direita e vice-versa
  tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)), 
  tf.keras.layers.Dense(64, activation="relu"),
  tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print("### Etapa 5 - Treinando a rede")
num_epochs = 30
history = model.fit(padded_treinamento, training_labels, epochs=num_epochs,
                    validation_data=(padded_teste, testing_labels), verbose=2)

print("\n### Etapa 6 - Salvando modelo e tokenizer")
# Salva o modelo treinado
model.save('modelo_sentimentos.h5')
print("Modelo salvo como 'modelo_sentimentos.h5'")

# Salva o tokenizer
import pickle
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("Tokenizer salvo como 'tokenizer.pickle'")

# Salva configurações
config = {
    'max_length': max_length,
    'padding_type': padding_type,
    'trunc_type': trunc_type
}
with open('config.pickle', 'wb') as handle:
    pickle.dump(config, handle, protocol=pickle.HIGHEST_PROTOCOL)
print("Configurações salvas como 'config.pickle'")

print("\n### Etapa 7 - Iniciando API Flask")
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Variáveis globais para modelo, tokenizer e config já carregados
# (foram criados durante o treinamento acima)
modelo_carregado = model
tokenizer_carregado = tokenizer
config_carregado = config

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
    app.run(host='0.0.0.0', port=5000, debug=True)
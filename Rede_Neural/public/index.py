from flask import Flask, request, render_template_string

app = Flask(__name__)


html_template = """
<!doctype html>
<html>
<head><title>Análise de Sentimentos</title></head>
<body>
  <h2>Digite um comentário:</h2>
  <form method="POST">
    <textarea name="comentario" rows="4" cols="50"></textarea><br>
    <input type="submit" value="Analisar">
  </form>
  {% if resultado %}
    <h3>Resultado: {{ resultado }}</h3>
  {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def sentiment():
    resultado = None
    if request.method == 'POST':
        texto = request.form['comentario']
        seq = tokenizer.texts_to_sequences([texto])
        pad = pad_sequences(seq, padding='post', maxlen=10)
        pred = model.predict(pad)[0][0]
        resultado = "Positivo" if pred > 0.5 else "Negativo"
    return render_template_string(html_template, resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
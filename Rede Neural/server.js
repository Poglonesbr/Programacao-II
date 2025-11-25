const express = require('express'); 
const path = require('path'); 
const app = express(); 

app.use(express.static(path.join(__dirname, 'public'))); 

app.post('/phrase', express.json(), (req, res) => {
    const { phrase } = req.body;
    console.log(`Frase recebida: ${phrase}`);
    res.json({ message: "Esta frase é ", sentimento," });
});


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
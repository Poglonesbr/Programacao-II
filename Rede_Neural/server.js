const express = require('express'); 
const path = require('path'); 
const { spawn } = require('child_process');
const app = express(); 

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

app.post('/analisar', (req, res) => {
    const { frase } = req.body;
    
    if (!frase) {
        return res.status(400).json({ erro: 'Frase não fornecida' });
    }
    
    console.log(`Analisando frase: ${frase}`);
    
    // Executa o script Python passando a frase como argumento
    const pythonPath = path.join(__dirname, '.venv', 'Scripts', 'python.exe');
    const scriptPath = path.join(__dirname, 'rede neural', 'analisar.py');
    
    // Executa o Python com diretório de trabalho apontando para a pasta do script
    const pythonCwd = path.join(__dirname, 'rede neural');
    const python = spawn(pythonPath, [scriptPath, frase], { cwd: pythonCwd });
    
    let dataString = '';
    let errorString = '';
    
    python.stdout.on('data', (data) => {
        dataString += data.toString();
    });
    
    python.stderr.on('data', (data) => {
        errorString += data.toString();
    });
    
    python.on('close', (code) => {
        console.log('Python exit code:', code);
        console.log('Python stdout:', dataString.slice(0, 2000));
        console.log('Python stderr:', errorString.slice(0, 2000));

        if (code !== 0) {
            console.error('Erro Python (exit', code, '):', errorString);
            return res.status(500).json({ erro: 'Erro ao processar análise', details: errorString });
        }
        
        if (!dataString || dataString.trim().length === 0) {
            console.error('Python não retornou saída em stdout');
            return res.status(500).json({ erro: 'Resposta vazia do Python', details: errorString });
        }

        try {
            const resultado = JSON.parse(dataString);
            return res.json({ resultados: [resultado] });
        } catch (e) {
            console.error('Erro ao parsear JSON:', e, dataString);
            return res.status(500).json({ erro: 'Erro ao processar resposta', details: dataString });
        }
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
    console.log(`Acesse: http://localhost:${PORT}`);
});
const phrase = document.querySelector('#phrase');
const submitButton = document.querySelector('#submitButton');
const output = document.querySelector('.output');

submitButton.addEventListener('click', async () => {
    const fraseTexto = phrase.value.trim();
    
    if (!fraseTexto) {
        alert('Por favor, digite uma frase!');
        return;
    }
    
    // Limpa resultado anterior
    output.textContent = 'Analisando...';
    
    try {
        // Envia para Node.js que chama o Python (usando caminho relativo)
        const response = await fetch('/analisar', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                frase: fraseTexto
            })
        });
        
        if (!response.ok) {
            throw new Error('Erro na resposta da API');
        }
        
        const data = await response.json();
        
        if (data.resultados && data.resultados.length > 0) {
            const resultado = data.resultados[0];
            const sentimento = resultado.sentimento;
            const probPositivo = (resultado.probabilidade_positivo * 100).toFixed(1);
            const probNegativo = (resultado.probabilidade_negativo * 100).toFixed(1);
            
            // Exibe resultado
            output.innerHTML = `
                <div class="panel resultado ${sentimento === 'Positivo' ? 'positivo' : 'negativo'}">
                  <h2>${sentimento}</h2>
                  <p class="meta">${resultado.frase}</p>
                  <p>Confiança: Pos ${probPositivo}% • Neg ${probNegativo}%</p>
                </div>
            `;
        } else {
            output.textContent = 'Erro: resposta inválida da API';
        }
        
    } catch (error) {
        console.error('Erro:', error);
        output.textContent = 'Erro ao analisar sentimento. Verifique se o servidor está rodando.';
        alert("Erro ao processar a requisição. Certifique-se de que o servidor Node.js está rodando na porta 3000.");
    }
})


const dateInput = document.querySelector('#dateInput');
const dateOutput = document.querySelector('#dateOutput');
const btnConv = document.querySelector('#btnConv');

const date1 = document.querySelector('#date1');
const date2 = document.querySelector('#date2');
const btnCompare = document.querySelector('#btnCompare');
const diffResult = document.querySelector('#diffResult');

// Função para converter data/timestamp
btnConv.addEventListener('click', () => {
    const input = dateInput.value;
    fetch(`/api/${encodeURIComponent(input)}`)
        .then(response => response.json())
        .then(data => {
            dateOutput.innerHTML = data.error ? 
                `<span class="error">${data.error}</span>` :
                `<strong>Unix:</strong> ${data.unix}<br>
                 <strong>UTC:</strong> ${data.utc}`;
        })
        .catch(() => {
            dateOutput.innerHTML = `<span class="error">Erro ao processar a requisição</span>`;
        });
});

// Função para comparar datas
btnCompare.addEventListener('click', () => {
    const d1 = encodeURIComponent(date1.value);
    const d2 = encodeURIComponent(date2.value);
    
    fetch(`/api/diff/${d1}/${d2}`)
        .then(response => response.json())
        .then(data => {
            diffResult.innerHTML = data.error ? 
                `<span class="error">${data.error}</span>` :
                `<strong>Diferença:</strong><br>
                 ${data.days} dias, ${data.hours} horas,
                 ${data.minutes} minutos, ${data.seconds} segundos`;
        })
        .catch(() => {
            diffResult.innerHTML = `<span class="error">Erro ao processar a requisição</span>`;
        });
});

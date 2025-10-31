const dateInput = document.querySelector('#dateInput');
const dateOutput = document.querySelector('#dateOutput');
const btnConv = document.querySelector('#btnConv');             // Aqui pega os elementos do html e joga pro js
const date1 = document.querySelector('#date1');
const date2 = document.querySelector('#date2');
const btnCompare = document.querySelector('#btnCompare');
const diffResult = document.querySelector('#diffResult');

btnConv.addEventListener('click', () => { // Função para converter data/timestamp
    const input = dateInput.value;          // Pega o valor do input (ou seja, a data ou timestamp que o usuário digitou)
    fetch(`/api/${(input)}`)                // Faz uma requisição pra API (ou seja, chama o arquivo que ta lá no servidor, que é o server.js)
        .then(response => response.json())      // Converte a resposta pra JSON (ou seja, transforma o arquivo que ta lá no servidor em um arquivo que o navegador consegue entender)
        .then(data => {                         // Aqui ta pegando a resposta (ou seja, o arquivo que ta lá no servidor) e transformando em um objeto JS (ou seja, um objeto que o navegador consegue entender)
            dateOutput.innerHTML = data.error ?     // Aqui ta verificando se a resposta tem erro se der só aparece a mensagem de erro, se não der erro continua o código
                `<span class="error">${data.error}</span>` :  // Transforma os dados para HTML o (${} é para colocar o valor da variável dentro do HTML)
                `<strong>Unix:</strong> ${data.unix}<br>
                 <strong>UTC:</strong> ${data.utc}<br>
                 <strong>Data Local:</strong> ${data.diaSemana}, ${data.utclocal}`;
        })
        .catch(() => {
            dateOutput.innerHTML = `<span class="error">Erro ao processar a requisição</span>`;  // Se der erro na requisição, aparece a mensagem de erro
        });
});

btnCompare.addEventListener('click', () => { // Função para comparar datas
    const d1 = date1.value;
    const d2 = date2.value;
    fetch(`/api/diff/${d1}/${d2}`)
        .then(response => response.json())
        .then(data => {
            diffResult.innerHTML = data.error ? 
                `<span class="error">${data.error}</span>` : // Aqui faz o mesmo dali de cima
                `<strong>Diferença:</strong><br>
                 ${data.days} dias, ${data.hours} horas,
                 ${data.minutes} minutos, ${data.seconds} segundos`;
        })
        .catch(() => {
            diffResult.innerHTML = `<span class="error">Erro ao processar a requisição</span>`;
        });
});

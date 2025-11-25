const phrase = document.querySelector('#phrase');
const submitButton = document.querySelector('#submitButton')

submitButton.addEventListener('click', async () => {
    try {
        const response = await fetch('/phrase', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                phrase: phrase.value
            })
        })
    } catch {
        alert("Erro ao processar a requisição");
    }
})
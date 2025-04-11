# Timestamp

## Objetivo do projeto

Desenvolver uma aplicação full-stack em JavaScript que implemente um microsserviço de timestamp, funcionalmente semelhante ao exemplo disponível em: Timestamp Microservice. Este projeto permitirá que você aplique conceitos de desenvolvimento web, manipulação de datas e APIs RESTful.

### Funcionalidades:
1. **Endpoint Principal**
    - **A API deve aceitar qualquer data que possa ser analisada corretamente pelo método new Date(date_string).**
    - **Uso e Exemplo:** Se a entrada for um timestamp Unix (exemplo: /api/1451001600000), a resposta deve ser: { "unix": 1451001600000, "utc": "Fri, 25 Dec 2015 00:00:00 GMT" }
    - **Erros:** Se a data for inválida, a API deve retornar o seguinte objeto JSON:{ "error": "Invalid Date" }
    - **Campo Vazio**Se nenhum parâmetro de data for fornecido, a API deve retornar o timestamp atual tanto em unix quanto em utc.
    - **Fuso Horários** A API deve suportar a conversão de fusos horários, permitindo que o usuário envie uma query string opcional para definir um fuso horário específico.

2. **Endpoint adicional**: `/api/diff/{date1}/{date2}`
   - Calcula a diferença entre duas datas em dias, horas, minutos e segundos.

Criar um frontend básico para testar e visualizar os resultados da API de forma interativa.

## Passo a Passo de Execução

**1. Clonar o Repositório ou Sair da Pasta Geral:**
   Primeiro, você precisa clonar o repositório para o seu ambiente local.
   ```sh
   git https://github.com/Poglonesbr/Programacao-II.git
   cd Programa-o-II
   ```
   ou pode utilizar do arquivo .zip mas utilizando o comando 
   ```sh
   cd Programa-o-II
   ```
   ou pode utilizar do arquivo .zip mas removendo a pasta 
   ```sh
   Programacao-II-main
   ```


**2. Instalar Dependências:**
   Instale as dependências do projeto usando npm.
   ```sh
   npm install
   ```

**3. Iniciar o Servidor:**
   Inicie o servidor Node.js.
   ```sh
   npm run start
   ```
   Isso vai iniciar o servidor na porta 3000.

**4. Acessar a Aplicação:**
   Abra o navegador e acesse a URL:
   ```
   http://localhost:3000
   ```
   Isso carregará a página principal da aplicação que serve o arquivo `index.html`.

**É isso, muito obrigado por ver**
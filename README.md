# Resumidor de Texto

## Descrição
O **Resumidor de Texto** é uma aplicação desenvolvida para resumir textos da Wikipedia de acordo com uma quantidade expecificada de palavras. Utilizando a API da OpenAI, a aplicação permite que os usuários obtenham resumos de conteúdos extensos.

## Requisitos
- **Docker Compose**
- **Python**: para executar localmente
- **Chave da OpenAI**: Você deve ter uma chave de API da OpenAI com quotas ativas

## Como Rodar o Projeto com Docker Compose
1. **Clone o repositório**:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd resumidorTexto
   ```

2. **Altere o arquivo `.env`**:
   - No arquivo `.env`, informar um valor para a variável `OPENAI_API_KEY` com uma chave de API da OpenAI que possua quotas. O .env está na raiz do projeto.

3. **Subindo a aplicação**:
   - Executar o comando para iniciar a aplicação e o banco de dados PostgreSQL:
   ```bash
   docker-compose up --build
   ```

4. **Acessando a API**:
   A API estará disponível na seguinte URL:
   ```
   http://localhost:8080/resumos
   ```

## Executando o Projeto pelo PyCharm

1. **Editar/Criar Configurações**:
   - Em editar configurações, adicionar uma nova configuração em Python.

2. **Configurar o módulo**:
   - Selecione o módulo `uvicorn` como o seu script de execução.

3. **Definir os parâmetros do script**:
   - Adicione os seguintes parâmetros no script:
   ```plaintext
   app.main:app --reload --host 0.0.0.0 --port 8080
   ```

4. **Configurar variáveis de ambiente**:
   - Mude a variável `POSTGRES_HOSTNAME` para `localhost`.
   - Aponte o caminho do arquivo `.env` para o seguinte:
   ```plaintext
   .../resumidorTexto/.env
   ```

## Monitoramento com Prometheus
A aplicação inclui monitoramento utilizando o Prometheus. O Prometheus estará acessível na porta `9090`. Para acessar a interface do Prometheus, você pode visitar:
```
http://localhost:9090
```

## Portas
- **API**: `8080`
- **PostgreSQL**: `5432`
- **Prometheus**: `9090`

## Coleção de Exemplos
Uma collection de exemplos para testar a API está disponível na pasta `collection` do projeto, sendo possível importar no Insomnia para efetuar as requisições.

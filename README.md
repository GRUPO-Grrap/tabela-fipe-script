# Tabela FIPE Script

Este projeto é um script Python que se conecta a um banco de dados PostgreSQL para inserir dados de um arquivo `.csv`.

## 🚀 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- Gerenciador de pacotes `pip`

## 📦 Instalação

1. **Clone este repositório:**

   ```sh
   git clone https://github.com/GRUPO-Grrap/tabela-fipe-script
   cd tabela-fipe-script
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

   ```sh
   python -m venv venv
   # Ativar o ambiente virtual
   # No Windows:
   venv\Scripts\activate
   # No macOS/Linux:
   source venv/bin/activate
   ```

3. **Instale as dependências do projeto:**

   ```sh
   pip install -r requirements.txt
   ```

## ⚙️ **Configuração do Banco de Dados**

    user=
    password=
    host=
    port=
    database=
    table_name=

## ▶️ Executando o Script

Após configurar o banco de dados, execute o script com:

```sh
python main.py
```

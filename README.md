QuickFundHub
QuickFundHub é uma aplicação desenvolvida para facilitar a integração com serviços de troca de dados financeiros. Utilizando o Streamlit, a aplicação oferece uma interface intuitiva para visualizar e analisar dados financeiros armazenados no AWS S3. Com suporte para conexões seguras e gerenciamento eficiente de credenciais, QuickFundHub permite que os usuários acessem e manipulem dados de forma rápida e segura.

Características Principais
Integração com AWS S3: Acesso seguro a arquivos armazenados no Amazon S3.
Visualização de Dados: Interface amigável para visualização e análise de dados financeiros.
Gerenciamento de Credenciais: Uso de Streamlit Secrets para garantir a segurança das credenciais.
Cache de Resultados: Armazenamento em cache para melhorar a performance e reduzir o tempo de resposta.
Requisitos
Python 3.7 ou superior
Streamlit
s3fs
st-files-connection
Instalação
Clone o repositório:

git clone https://github.com/tjmendes/hubquickfund1.git
cd hubquickfund1
Crie um ambiente virtual e ative-o:

python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
Instale as dependências:

pip install -r requirements.txt
Configure suas credenciais da AWS no arquivo .streamlit/secrets.toml:

# .streamlit/secrets.toml
AWS_ACCESS_KEY_ID = "sua_chave_de_acesso"
AWS_SECRET_ACCESS_KEY = "sua_chave_secreta"
AWS_DEFAULT_REGION = "sua_regiao"
Uso
Inicie o aplicativo Streamlit:

streamlit run app.py
Acesse o aplicativo no seu navegador em http://localhost:8501.

Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorias e correções.

Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


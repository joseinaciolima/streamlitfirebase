from dotenv import load_dotenv
import os
import json
import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

# Carregar o arquivo .env explicitamente (use o caminho correto)
load_dotenv()

# Carregar o caminho do arquivo de credenciais do Firebase a partir do .env
cred_path = os.getenv('FIREBASE_CREDENTIALS_JSON')


# Se o caminho estiver None, exibir um erro
if cred_path is None:
    st.error("A variável de ambiente 'FIREBASE_CREDENTIALS_JSON' não foi encontrada no arquivo .env.")

# Verifique se o Firebase já foi inicializado
if not firebase_admin._apps:
    if cred_path and os.path.exists(cred_path):
        try:
            # Abrir e carregar o conteúdo JSON do arquivo de credenciais
            with open(cred_path) as f:
                cred_dict = json.load(f)
                cred = credentials.Certificate(cred_dict)

            # Inicializar o Firebase
            firebase_admin.initialize_app(cred)
            st.success("Firebase inicializado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao inicializar o Firebase: {str(e)}")
            st.stop()
    else:
        st.error("Arquivo de credenciais do Firebase não encontrado.")
        st.stop()

# Interface de login/signup com Streamlit
choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])

if choice == 'Login':
    email = st.text_input('Email Address')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        # Aqui você pode implementar a lógica de login usando Firebase Authentication
        st.write("Tentativa de login...")

else:
    email = st.text_input('Email Address')
    password = st.text_input('Password', type='password')
    username = st.text_input('Entre seu username')

    if st.button('Criar minha conta'):
        try:
            # Tentar criar o usuário no Firebase
            user = auth.create_user(email=email, password=password, uid=username)
            st.success('Conta criada com sucesso!')
            st.markdown('Por favor faça Login usando seu email e senha')
            st.balloons()
        except Exception as e:
            st.error(f"Erro ao criar a conta: {str(e)}")





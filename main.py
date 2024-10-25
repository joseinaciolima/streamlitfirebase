import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st
import json

# Carregar as credenciais do Firebase diretamente dos segredos
try:
    firebase_config = st.secrets["firebase"]
except KeyError:
    st.error("Credenciais do Firebase não encontradas nos segredos.")
    st.stop()

# Converter as strings do toml para um dicionário JSON
firebase_config_dict = {
    "type": firebase_config["type"],
    "project_id": firebase_config["project_id"],
    "private_key_id": firebase_config["private_key_id"],
    "private_key": firebase_config["private_key"].replace("\\n", "\n"),  # Corrigir quebras de linha na chave privada
    "client_email": firebase_config["client_email"],
    "client_id": firebase_config["client_id"],
    "auth_uri": firebase_config["auth_uri"],
    "token_uri": firebase_config["token_uri"],
    "auth_provider_x509_cert_url": firebase_config["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_config["client_x509_cert_url"]
}

# Verifique se o Firebase já foi inicializado
if not firebase_admin._apps:
    try:
        # Inicializar o Firebase usando as credenciais convertidas
        cred = credentials.Certificate(firebase_config_dict)
        firebase_admin.initialize_app(cred)
        st.success("Firebase inicializado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao inicializar o Firebase: {str(e)}")
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


import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def load_config(path="config.yaml"):
    with open(path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def authenticate():
    config = load_config()

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )

    name, authentication_status, username = authenticator.login("Connexion", "main")

    if authentication_status:
        authenticator.logout("Déconnexion", "sidebar")
        st.sidebar.write(f'Bienvenue *{name}* !')
        return True, username
    elif authentication_status is False:
        st.error('Nom d’utilisateur ou mot de passe incorrect')
    elif authentication_status is None:
        st.warning('Veuillez saisir vos identifiants')
    return False, None

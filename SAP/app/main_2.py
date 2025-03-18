import streamlit as st
import pandas as pd
from database import Database
from auth import authenticate
from sap_connector import SAPConnector

st.set_page_config(page_title="CRUD SAP BW", layout="wide")

# Authentification utilisateur
auth_status, username = authenticate()

if auth_status:
    # Votre code Streamlit original ici après authentification réussie
    st.title(f"📊 Application CRUD - SAP BW (Utilisateur : {username})")

    # Connexion DB et SAP
    db = Database("sqlite:///data/local_data.db")
    sap = SAPConnector()

    table_name = st.sidebar.selectbox("Sélectionnez la table", ["clients", "ventes", "stocks"])

    st.subheader(f"Gestion des données : {table_name.capitalize()}")

    data = db.read(table_name)
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

    # (Ici intégrer le reste de votre code CRUD et SAP existant)

    # Interface CRUD
    st.sidebar.subheader("Créer un nouvel enregistrement")
    with st.sidebar.form("create_record"):
        new_data = {}
        for column in df.columns:
            if column != "id":
                new_data[column] = st.text_input(f"{column}")
        submit_create = st.form_submit_button("Créer")
        if submit_create:
            create_record(table_name, new_data)
            st.success("Enregistrement créé avec succès !")

    st.sidebar.subheader("Modifier un enregistrement existant")
    record_id_to_update = st.sidebar.number_input("ID à modifier", step=1)
    with st.sidebar.form("update_record"):
        updated_data = {}
        for column in df.columns:
            if column != "id":
                updated_data[column] = st.text_input(f"Nouveau {column}")
        submit_update = st.form_submit_button("Mettre à jour")
        if submit_update:
            update_record(table_name, record_id_to_update, updated_data)
            st.success("Enregistrement mis à jour !")

    st.sidebar.subheader("Supprimer un enregistrement")
    record_id_to_delete = st.sidebar.number_input("ID à supprimer", step=1)
    if st.sidebar.button("Supprimer"):
        delete_record(table_name, record_id_to_delete)
        st.warning("Enregistrement supprimé !")


else:
    st.stop()

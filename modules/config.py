import os

def get_secret(key):
    try:
        import streamlit as st
        return st.secrets[key]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv(key)
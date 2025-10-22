import streamlit as st # Visualises data in Streamlit Cloud
import ee # Earth Engine python library
from google.oauth2 import service_account 
from ee import oauth
import geemap.foliumap as geemap 
from streamlit import errors # import errors library

def ee_to_st():
    """
    Authenticate Earth Engine using a service account on Streamlit Cloud.
    """
    try:
        service_account_keys = st.secrets["ee_keys"]
        credentials = service_account.Credentials.from_service_account_info(
                            service_account_keys, scopes=oauth.SCOPES
                            )
        ee.Initialize(credentials)
        geemap.ee_initialize()

        return "Successfully authenticated with Google Earth Engine"
    except errors.StreamlitSecretNotFoundError:
        return geemap.ee_initialize()

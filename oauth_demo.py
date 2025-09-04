import streamlit as st
import requests
import os
import urllib.parse

# Configuración (REEMPLAZA con tus credenciales)
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8501"  # Asegúrate de que coincida con la configuración en Google Cloud
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
SCOPE = ["profile", "email"]

# Estado de la sesión
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# Si no hay token, mostrar el botón de inicio de sesión
if not st.session_state.access_token:
    # Crear la URL de autorización
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPE),
        'access_type': 'offline',  # Para obtener un refresh token (opcional)
        'prompt': 'consent',  # Para forzar la solicitud de consentimiento (opcional)
    }
    authorize_url = AUTHORIZE_URL + '?' + urllib.parse.urlencode(params)

    st.markdown(f'<a href="{authorize_url}">Iniciar sesión con Google</a>', unsafe_allow_html=True)

    # Obtener el código de autorización de la URL
    code = st.query_params.get('code')

    if code:
        # Intercambiar el código por un token de acceso
        data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        response = requests.post(TOKEN_URL, data=data)
        token_info = response.json()

        if 'access_token' in token_info:
            st.session_state.access_token = token_info['access_token']
            st.session_state.refresh_token = token_info.get('refresh_token')  # Guardar el refresh token (opcional)
            st.success('¡Inicio de sesión exitoso!')
            st.rerun()
        else:
            st.error('Error al obtener el token de acceso.')
            st.write(token_info)  # Mostrar información de error
else:
    # Si hay token, mostrar la información del usuario
    st.success('¡Has iniciado sesión!')
    # Llamar a la API de Google para obtener información del usuario (ejemplo)
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {st.session_state.access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    st.write('Información del usuario:', user_info)

    st.write("Contenido PREMIUM aquí...")
    st.balloons()

    # Botón de cierre de sesión
    if st.button('Cerrar sesión'):
        st.session_state.access_token = None
        st.rerun()
        # Este es un comentario de prueba para verificar la conexión con GitHub.
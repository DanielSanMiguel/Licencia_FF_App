# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:42:28 2024

@author: Daniel
"""

import streamlit as st
import requests
import json
import re

def validar_correo(email):
    # Expresión regular para correos electrónicos
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(patron, email):
        return True
    else:
        return False

# Definir el estilo CSS para cambiar el color de fondo
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, #323232, #6a6a6a, #b2b1b1, #6a6a6a, #323232);
    }
</style>
"""
custom_css = """
<style>
div[data-baseweb="input"] {
    background-color: #848282;
    margin: none;
    border: none;
    }
div[data-baseweb="base-input"] {
    background-color: #848282;
    margin: none;
    border: none;
    }
div[data-baseweb="base-input"] input {
    background-color: #c7c7c7;  /* Fondo color  */
    border: 3px solid #0f0f0f;  /* Borde color  */
    border-radius: 10px;        /* Bordes redondeados */
    padding: 10px;              /* Espaciado interno */
    font-size: 16px;            /* Tamaño de fuente */
    margin: 1px ;
    }
</style>
"""
button_css = """
<style>

div[class="stButton"] button {
    
    border: none;
    background: radial-gradient(circle, #a0ff8b, #6dfe4d, #2eff00);
    color: black;
    }

</style>
"""
mkContainer = """
<style>
div[class="st-emotion-cache-1wmy9hl e1f1d6gn1"] {
    border: none;
    background-color: #848282;
    }

div[class="st-emotion-cache-1rsyhoq e1nzilvr5"] p {
    
    border: none;
    background: radial-gradient(circle, #fe603a, #fefb3a, #fe603a);
    color: black;
    }

</style>
"""
# Agregar el estilo a la app
st.markdown(page_bg_css, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(button_css, unsafe_allow_html=True)
st.markdown(mkContainer, unsafe_allow_html=True)

url_imagen_github_1 = "https://raw.githubusercontent.com/DanielSanMiguel/Licencia_FF_App/main/logo.jpg"


pag = st.empty()
contrasena_correcta = st.secrets['contrasena_correcta']
pag.title("Aplicación Protegida con Contraseña")
contrasena = pag.text_input("Ingrese la contraseña:", type="password")
if contrasena == contrasena_correcta:
    pag.success("¡Contraseña correcta! Bienvenido a la aplicación.")
    pag.empty()
    with pag.container():
        admin_password = st.secrets['admin_password']
        col_a, col_b, col_c = st.columns(3)
        # Título de la aplicación
        st.title("Licencia App Fly-Fut")
        with col_b:
            
            st.image(url_imagen_github_1, use_column_width=False)   
        # Entrada para la URL
        url = " https://flyfut.olocip.com/licenses/create"
        
        # Datos del usuario
        nombre = st.text_input("Nombre y Apellidos", "")
        club = st.text_input("Club", "")
        puesto = st.text_input("Puesto/Cargo", "")
        email = st.text_input("E-mail", "")
        
        # Campos de entrada para el cuerpo de la solicitud
        
        nombre_licencia = st.text_input("Nombre licencia (Ejemplo: Juan1)", "")
        
        # Datos y credenciales AT
        api_key = st.secrets['at_token']
        base_id = 'appjPY2KlFg6bpcT1'
        table_name = 'List_licencias'
        url_at = 'https://api.airtable.com/v0/appjPY2KlFg6bpcT1/List_licencias'
        
        headers_at = {"Authorization" : f"Bearer {api_key}",  "Content-Type" : 'application/json' }

        # Botón para enviar la solicitud
        col1, col2, col3 = st.columns(3)
        with col2:
            if validar_correo(email) and nombre and club and puesto and email and nombre_licencia:
                if st.button("Solicitar 7 días de prueba"):
                    # Cuerpo de la solicitud en formato JSON
                    data = {
                        'name': nombre_licencia
                    }
                
                    # Encabezados (headers)
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'admin_name': 'flyfut',
                        'admin_password': admin_password
                        
                    }
                    json.dumps(data)
                    # Realizar la solicitud POST
                    try:
                        
                        response = requests.post(url, data=data, headers=headers)
                
                        # Mostrar los resultados
                        st.subheader("Resultado de la solicitud:")
                        st.code(f"Código de estado: {response.status_code}")
                        data_at = {"records": [{"fields": {
                            'Nombre':nombre, 'Club':club, 'Puesto':puesto, 'Email':email, 'Licencia': response.json()['newLicense']}}]}
                        response_at = requests.post(url_at, json.dumps(data_at), headers=headers_at)
                        # Mostrar la respuesta en formato JSON si es posible
                        try:
                            st.write(response.json())
                        except json.decoder.JSONDecodeError:
                            st.write(response.text)
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error al enviar la solicitud: {e}")
            else:
                st.warning("Por favor, rellena todos los campos para habilitar el botón de envío.")
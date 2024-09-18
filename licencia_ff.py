# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:42:28 2024

@author: Daniel
"""

import streamlit as st
import requests
import json
import re
import pandas as pd
from airtable import Airtable

def validar_correo(email):
    # Expresión regular para correos electrónicos
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(patron, email):
        return True
    else:
        return False

def convert_to_dataframe(airtable_records):
    """Converts dictionary output from airtable_download() into a Pandas dataframe."""
    airtable_rows = []
    airtable_index = []
    for record in airtable_records['records']:
        airtable_rows.append(record['fields'])
        airtable_index.append(record['id'])
    airtable_dataframe = pd.DataFrame(airtable_rows, index=airtable_index)
    return airtable_dataframe

# Datos y credenciales AT
api_key = st.secrets['at_token']
base_id = 'appjPY2KlFg6bpcT1'
table_name = 'List_licencias'
url_at = 'https://api.airtable.com/v0/appjPY2KlFg6bpcT1/List_licencias'
headers_at = {"Authorization" : f"Bearer {api_key}",  "Content-Type" : 'application/json' }

at_Table1 = Airtable(base_id, api_key)
# recuperamos datos de la tabla
result_at_Table1 = at_Table1.get(table_name)
# convertimos a DataFrame de Pandas
df = convert_to_dataframe(result_at_Table1)
try:
    lista_mail= df['Email'].tolist()
except:
    lista_mail=[]


custom_css = """
<style>
div[data-baseweb="input"] {
    background-color: transparent;
    margin: none;
    border: none;
    }
div[data-baseweb="base-input"] {
    background: linear-gradient(to left, #b0aead, #c9c7c5, #dddbd8, #c9c7c5, #b0aead);
    margin: none;
    border: none;
    }
div[data-baseweb="base-input"] input {
    background: linear-gradient(to left, #b0aead, #c9c7c5, #dddbd8, #c9c7c5, #b0aead);
    background-color: transparent;
    border: 3px solid #0f0f0f;  /* Borde color  */
    border-radius: 10px;        /* Bordes redondeados */
    padding: 10px;              /* Espaciado interno */
    font-size: 16px;            /* Tamaño de fuente */
    margin: none ;
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
div[data-testid="stAlertContainer"] {
    margin: none;
    border: none;
    background-color: transparent;
    }

div[class="st-emotion-cache-1rsyhoq e1nzilvr5"] p {
    
    border: none;
    background-color: transparent;
    color: black;
    font-size: large;
    }

</style>
"""
# Agregar el estilo a la app
#st.markdown(custom_css, unsafe_allow_html=True)
#st.markdown(button_css, unsafe_allow_html=True)
#st.markdown(mkContainer, unsafe_allow_html=True)

url_imagen_github_1 = "https://raw.githubusercontent.com/DanielSanMiguel/Licencia_FF_App/main/foto_ff_cut.jpg"
logo = "https://raw.githubusercontent.com/DanielSanMiguel/Licencia_FF_App/main/logo.jpg"
admin_password = st.secrets['admin_password']
# Entrada para la URL
url = " https://flyfut.olocip.com/licenses/create"

st.set_page_config(
    page_title="Fly-Fut Analytics",  # Título de la pestaña
    page_icon=logo,      # Puedes usar un emoji o una imagen
)
with st.container():
    # Título de la aplicación
    st.title("Licencia Fly-Fut Analytics")
    st.subheader('Rellena todos los campos para enviar el formulario')
    st.image(url_imagen_github_1, use_column_width='auto')

    # Datos del usuario
    nombre = st.text_input("Nombre y Apellidos", "")
    club = st.text_input("Club", "")
    puesto = st.text_input("Puesto/Cargo", "")
    email = st.text_input("E-mail", "")
    ya_existe = False
    if email in lista_mail:
        st.write(':warning: Correo ya vinculado a licencia, prueba con otro correo.')
        ya_existe = True
    
    # Campos de entrada para el cuerpo de la solicitud
    nombre_licencia = nombre
    
    # Botón para enviar la solicitud
    col1, col2, col3 = st.columns(3)
   
    if validar_correo(email) and nombre and club and puesto and email and nombre_licencia and ya_existe==False:
        with col2:
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
                    data_at = {"records": [{"fields": {
                        'Nombre':nombre, 'Club':club, 'Puesto':puesto, 'Email':email, 'Licencia': response.json()['newLicense']}}]}
                    response_at = requests.post(url_at, json.dumps(data_at), headers=headers_at)
                    # Mostrar la respuesta en formato JSON si es posible
                    st.write('En breve se enviará un mail a la dirección que has facilitado con el número de licencia y las instrucciones, gracias.')

                except requests.exceptions.RequestException as e:
                    st.error(f"Error al enviar la solicitud: {e}")
    else:
        st.warning("Por favor, rellena todos los campos para habilitar el botón de envío.")

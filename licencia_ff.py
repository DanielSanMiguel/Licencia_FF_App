# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 13:42:28 2024

@author: Daniel
"""

import streamlit as st
import requests
import json

pag = st.empty()
contrasena_correcta = st.secrets['contrasena_correcta']
pag.title("Aplicación Protegida con Contraseña")
contrasena = pag.text_input("Ingrese la contraseña:", type="password")
if contrasena == contrasena_correcta:
    pag.success("¡Contraseña correcta! Bienvenido a la aplicación.")
    pag.empty()
    with pag.container():
        admin_password = st.secrets['admin_password']
        # Título de la aplicación
        st.title("Licencia App Fly-Fut")
        
        # Entrada para la URL
        url = " https://flyfut.olocip.com/licenses/create"
        
        # Campos de entrada para el cuerpo de la solicitud
        
        nombre = st.text_input("Nombre", "Introduzca su nombre")
        
        # Botón para enviar la solicitud
        if st.button("Enviar solicitud"):
            # Cuerpo de la solicitud en formato JSON
            data = {
                'name': nombre
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
                
                # Mostrar la respuesta en formato JSON si es posible
                try:
                    st.json(response.json())
                except json.decoder.JSONDecodeError:
                    st.write(response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Error al enviar la solicitud: {e}")
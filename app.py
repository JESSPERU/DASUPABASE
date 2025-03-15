import streamlit as st
from supabase import create_client, Client
import os

# Cargar variables de entorno
SUPABASE_URL =  "https://pipplgjnsnycifhnrahr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpcHBsZ2puc255Y2lmaG5yYWhyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE3NDU3MTcsImV4cCI6MjA1NzMyMTcxN30.wwUhzhNA8bMknz3rM7pcA0tCUlCz7H663UsZzmlYvhw"

# Conectar con Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#titulo streamlit
st.title("Gestion de clientes CRUD con supabase y streamlit")

st.header("Agregar cliente")
nombre = st.text_input("Nombre")
email = st.text_input("E-mail")
telefono= st.text_input("Teléfono")

if st.button(f"✍️ agregar cliente"):
    if nombre and email:
        data = {"nombre" : nombre, "email" : email, "telefono" : telefono}
        response = supabase.table("clientes").insert(data).execute()
        st.success("Cliente agregado correctamente ")
    else:
        st.warning("Nombre e email son obligatorios")    

st.header("Clientes registrados")
clientes = supabase.table("clientes").select("*").execute()

if clientes.data:
    for cliente in clientes.data:
        with st.expander (cliente["nombre"]):
            st.write(f"📧 {cliente['email']}")
            st.write(f"📞 {cliente['telefono']}")
            st.write(f"📅Fecha de registro: {cliente['fecha_registro']}")

            if st.button(f"❌ Eliminar {cliente['nombre']}", key=cliente["id"]):
                supabase.table("clientes").delete().eq("id", cliente["id"]).execute()
                st.success(f"{cliente['nombre']} eliminado correctamente")
                st.rerun()


            #FORMULARIO PARA ACTUALIZAR CLIENTE

            st.subheader("Actualizar Cliente")
            nuevo_nombre = st.text_input("Nuevo Nombre", value=cliente["nombre"], key=f"nombre_{cliente['id']}")    
            nuevo_email = st.text_input("Nuevo email", value=cliente["email"], key=f"email_{cliente['id']}")
            nuevo_telefono = st.text_input("Nuevo teléfono", value=cliente["telefono"], key=f"telefono_{cliente['id']}")

            if st.button("Actualizar", key=f"upd_{cliente['id']}"):
                supabase.table("clientes").update({
                    "nombre": nuevo_nombre,
                    "email": nuevo_email,
                    "telefono": nuevo_telefono
                }).eq("id", cliente ["id"]).execute()

                st.success(f"{cliente ['nombre']} actualizado correctamente")
                st.rerun()

else:
    st.info("No hay clientes registrados aún")
import streamlit as st
import hashlib
import pandas as pd
import os

st.set_page_config(page_title="Iniciar sesión | QOMI", layout="centered")

# Estilos personalizados
st.markdown("""
    <style>
    .login-box {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .login-box h2 {
        text-align: center;
        margin-bottom: 10px;
    }
    .login-box small {
        display: block;
        text-align: center;
        margin-bottom: 20px;
        color: #666;
    }
    .login-box input {
        width: 100%;
        padding: 10px;
        margin-bottom: 15px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .login-box button {
        width: 100%;
        padding: 10px;
        background-color: #333;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .login-box button:hover {
        background-color: #111;
    }
    .login-box .extra-links {
        text-align: center;
        margin-top: 10px;
    }
    .social-login {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
    }
    .social-login img {
        width: 32px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# =================== LÓGICA DE AUTENTICACIÓN ===================

USUARIOS_PATH = "usuarios.xlsx"
if os.path.exists(USUARIOS_PATH):
    df_usuarios = pd.read_excel(USUARIOS_PATH)
else:
    df_usuarios = pd.DataFrame(columns=["usuario", "password_hash"])
    df_usuarios.to_excel(USUARIOS_PATH, index=False)

def autenticar(usuario, password):
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = df_usuarios[df_usuarios["usuario"] == usuario]
    return not user.empty and user.iloc[0]["password_hash"] == password_hash

# =================== FORMULARIO ===================
with st.container():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h2>Iniciar sesión</h2>", unsafe_allow_html=True)
    st.markdown("<small>¿Es tu primera vez? <a href='#'>Regístrate</a></small>", unsafe_allow_html=True)

    usuario = st.text_input("Email", placeholder="Ej. nombre@correo.com")
    password = st.text_input("Contraseña", type="password", placeholder="Tu contraseña")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("&nbsp;", unsafe_allow_html=True)
    with col2:
        st.markdown("[:blue[_¿Olvidaste tu contraseña?_]](#)", unsafe_allow_html=True)

    if st.button("Iniciar sesión"):
        if not usuario or not password:
            st.warning("⚠️ Debes completar todos los campos.")
        elif autenticar(usuario, password):
            st.success("✅ Acceso exitoso. Bienvenido.")
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos.")

    st.markdown("<div class='extra-links'>o conéctate con</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='social-login'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174848.png' alt='Facebook'>
            <img src='https://cdn-icons-png.flaticon.com/512/281/281764.png' alt='Google'>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
#------------------------------------------------------------------------------------------------------------


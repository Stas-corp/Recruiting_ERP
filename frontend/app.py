import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.api_client import APIClient
from utils.state import init_session_state
from config import API_URL

st.set_page_config(page_title="HR Platform", page_icon="👥", layout="wide")
init_session_state()

def main():
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.title("👥 HR Platform")
    
    if "token" not in st.session_state or not st.session_state.token:
        st.info("🔐 Пожалуйста, авторизуйтесь")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Вход")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Пароль", type="password", key="login_password")
            if st.button("Вход"):
                api = APIClient(base_url=API_URL)
                result = api.login(email, password)
                if result:
                    st.session_state.token = result.get("access_token")
                    st.session_state.user = result.get("user")
                    st.rerun()
        with col2:
            st.subheader("Регистрация")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Пароль", type="password", key="reg_password")
            reg_name = st.text_input("ФИО", key="reg_name")
            if st.button("Регистрация"):
                api = APIClient(base_url=API_URL)
                result = api.register(reg_email, reg_password, reg_name)
                if result:
                    st.success("✅ Зарегистрированы! Теперь авторизуйтесь.")
        return
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📋 Навигация")
        page = st.radio("Выберите страницу:", ["🏠 Dashboard", "👤 Кандидаты", "📩 Отклики", "💼 Вакансии"])
        st.markdown("---")
        if "user" in st.session_state:
            st.markdown(f"**👤 {st.session_state.user.get('full_name', 'Unknown')}**")
        if st.button("🚪 Выход"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    if page == "🏠 Dashboard":
        st.header("Dashboard")
        st.info("Dashboard страница")
    elif page == "👤 Кандидаты":
        st.header("Кандидаты")
        st.info("Управление кандидатами")
    elif page == "📩 Отклики":
        st.header("Отклики")
        st.info("Управление откликами")
    elif page == "💼 Вакансии":
        st.header("Вакансии")
        st.info("Управление вакансиями")

if __name__ == "__main__":
    main()

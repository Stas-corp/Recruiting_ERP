import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.api_client import APIClient
from utils.state import init_session_state
from config import API_URL

pages = [
    st.Page("pages/_1_dashboard.py", title="Main Page", icon="🏠"),
    st.Page("pages/_2_candidates.py", title="Candidates", icon="👥"),
    st.Page("pages/_3_responses.py", title="Responses", icon="📋"),
    st.Page("pages/_4_vacancies.py", title="Vacancies", icon="💼"),
    # st.Page("pages/_5_analytics.py", title="Analytics", icon="📈"),
    # st.Page("pages/_6_users.py", title="Users", icon="🔐"),
    # st.Page("pages/_7_audit_logs.py", title="Audit Logs", icon="📝"),
]

st.set_page_config(page_title="HR Platform", page_icon="👥", layout="wide")
init_session_state()


def show_login_register():
    """Экран для неавторизованных пользователей"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Вход")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Пароль", type="password", key="login_password")
        if st.button("Вход", key="login_btn"):
            api = APIClient(base_url=API_URL)
            result = api.login(email, password)
            if result:
                st.session_state.token = result.get("access_token")
                st.session_state.user = result.get("user")
                st.success("✅ Вход выполнен!")
                st.rerun()
            else:
                st.error("❌ Неверные учетные данные")
    
    # with col2:
    #     st.subheader("📝 Регистрация")
    #     reg_email = st.text_input("Email", key="reg_email")
    #     reg_password = st.text_input("Пароль", type="password", key="reg_password")
    #     reg_name = st.text_input("ФИО", key="reg_name")
    #     if st.button("Регистрация", key="reg_btn"):
    #         api = APIClient(base_url=API_URL)
    #         result = api.register(reg_email, reg_password, reg_name)
    #         if result:
    #             st.success("✅ Зарегистрированы! Теперь авторизуйтесь.")
    #         else:
    #             st.error("❌ Ошибка при регистрации")


def show_sidebar():
    """Sidebar с навигацией (только для авторизованных)"""
    with st.sidebar:
        st.divider()
        if "user" in st.session_state:
            st.markdown(f"**👤 {st.session_state.user.get('full_name', 'Unknown')}**")
        
        if st.button("🚪 Выход", key="logout_btn", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    nav = st.navigation(pages)
    nav.run()


def main():
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.title("👥 HR Platform")
    
    is_authenticated = "token" in st.session_state and st.session_state.token
    
    if not is_authenticated:
        st.info("🔐 Пожалуйста, авторизуйтесь для доступа к платформе")
        show_login_register()
    else:
        show_sidebar()


if __name__ == "__main__":
    main()

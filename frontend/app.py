import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.api_client import APIClient
from utils.state import init_session_state
from config import API_URL

st.set_page_config(
    page_title="Recruiting Platform",
    page_icon="👥",
    layout="wide"
)

init_session_state()


def show_login():
    """Экран для неавторизованных пользователей"""
    st.title("👥 Recruiting Platform")
    st.info("🔐 Будь ласка, авторизуйтесь для доступу до платформи")
    
    col1, col2 = st.columns([0.6, 0.4])
    
    with col1:
        st.subheader("🔐 Вхід")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Пароль", type="password", key="login_password")
        
        if st.button("Вхід", key="login_btn"):
            if email and password:
                api = APIClient(base_url=API_URL)
                result = api.login(email, password)
                if result:
                    st.session_state.token = result.get("access_token")
                    st.session_state.user = result.get("user")
                    st.success("✅ Вхід виконано!")
                    st.rerun()
                else:
                    st.error("❌ Невірні облікові дані")
            else:
                st.warning("⚠️ Заповніть всі поля")


def show_app():
    """Главное приложение (для авторизованных)"""
    
    pages = [
        st.Page("app_pages/_1_dashboard.py", title="Main Page", icon="🏠"),
        st.Page("app_pages/_2_candidates.py", title="Candidates", icon="👥"),
        st.Page("app_pages/_3_responses.py", title="Responses", icon="📋"),
        # st.Page("app_pages/_4_vacancies.py", title="Vacancies", icon="💼"),
        # st.Page("app_pages/_5_analytics.py", title="Analytics", icon="📈"),
        # st.Page("app_pages/_6_users.py", title="Users", icon="🔐"),
        # st.Page("app_pages/_7_audit_logs.py", title="Audit Logs", icon="📝"),
    ]
    
    with st.sidebar:
        st.title("👤 Профіль")
        if "user" in st.session_state:
            st.markdown(f"**{st.session_state.user.get('full_name', 'Unknown')}**")
            st.caption(st.session_state.user.get('email', ''))
        
        st.divider()
        
        if st.button("🚪 Вихід", use_container_width=True, key="logout_btn"):
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
    
    nav = st.navigation(pages)
    nav.run()


def main():
    is_authenticated = "token" in st.session_state and st.session_state.token
    
    if not is_authenticated:
        show_login()
    else:
        show_app()


if __name__ == "__main__":
    main()

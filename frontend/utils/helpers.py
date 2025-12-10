import streamlit as st
from typing import List

def init_page(
    title: str,
    icon: str = "📄",
    layout: str = "wide",
    required_roles: List[str] = None
):
    """
    Инициализирует страницу с проверками
    
    Args:
        title: Название страницы
        icon: Иконка (emoji)
        layout: "wide" или "centered"
        required_roles: Список требуемых ролей (опционально)
    """
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout=layout
    )
    
    # Проверка авторизации
    if "token" not in st.session_state or not st.session_state.token:
        st.error("⚠️ Вы не авторизованы!")
        st.stop()
    
    # Проверка ролей (опционально)
    if required_roles:
        user_role = st.session_state.user.get("role")
        if user_role not in required_roles:
            st.error(f"❌ Доступ запрещён! Требуется роль: {', '.join(required_roles)}")
            st.stop()
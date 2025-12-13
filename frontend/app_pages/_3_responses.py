from datetime import datetime

import pandas as pd
import streamlit as st

from utils.helpers import init_page
from utils.api_client import APIClient

init_page("Responses", "📋")
st.header("📋 Responses")

api = APIClient(token=st.session_state.get('token'))

@st.cache_data
def load_data():
    result = api._request('GET', 'responses/')
    result.update(time_request=datetime.now().strftime("%H:%M %d.%m.%Y"))
    return result

@st.cache_data
def load_response_detail(response_id: int):
    """Загружаем детальную информацию отклика"""
    return api._request('GET', f'responses/{response_id}')

api_response = load_data()

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Оновити таблицю"):
        load_data.clear()
        st.toast("Таблиця оновлена!")
        api_response = load_data()
    st.metric("Всього відгуків", api_response["total"])

with col2:
    st.metric("Дата оновлення таблиці", api_response["time_request"])

st.json(api_response)

table_data = []
for item in api_response["items"]:
    table_data.append({
        "ID": item.get("id"),
        "Статус": item.get("status"),
        "Джерело": item.get("source"),
        "Кандидат": item.get("candidate", {}).get("full_name", "N/A"),
        "Позиція": item.get("vacancy", {}).get("position", "N/A"),
        "Дата": item.get("response_date"),
    })

df = pd.DataFrame(table_data)

st.dataframe(
    df,
    width="content",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="responses_df",
)

st.divider()

selected_rows = st.session_state.get("responses_df", {}).get("selection", {}).get("rows", [])

if selected_rows:
    selected_idx = selected_rows[0]
    selected_response = api_response["items"][selected_idx]
    
    # Загружаем детальную информацию
    # selected_response = load_response_detail(response_id)
    
    if selected_response:
        st.subheader(f"Детали відклику #{selected_response.get('id')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Кандидат:** {selected_response.get('candidate', {}).get('full_name')}")
            st.info(f"**Email:** {selected_response.get('candidate', {}).get('email')}")
            st.info(f"**Телефон:** {selected_response.get('candidate', {}).get('phone')}")
            st.info(f"**Статус:** {selected_response.get('status')}")
        
        with col2:
            st.info(f"**Позиція:** {selected_response.get('vacancy', {}).get('position')}")
            st.info(f"**Dept:** {selected_response.get('vacancy', {}).get('department')}")
            st.info(f"**Місто:** {selected_response.get('vacancy', {}).get('city')}")
            st.info(f"**Дата:** {selected_response.get('response_date')}")
        
        st.subheader("📄 Інформація про кандидата")
        
        candidate = selected_response.get("candidate", {})
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Резюме:**\n{candidate.get('resume', 'N/A')}")
            st.write(f"**Досвід:**\n{candidate.get('experience', 'N/A')}")
        
        with col2:
            st.write(f"**Примітки:**\n{candidate.get('notes', 'N/A')}")
            if candidate.get('skills'):
                skills_badges = " ".join(
                    [f"`{skill}`" for skill in candidate.get('skills', [])]
                )
                st.write(f"**Навички:** {skills_badges}")
        
        st.subheader("💼 Деталі вакансії")
        vacancy = selected_response.get("vacancy", {})
        st.write(f"**Опис:** {vacancy.get('description', 'N/A')}")
        
        salary_min = vacancy.get('salary_min')
        salary_max = vacancy.get('salary_max')
        if salary_min or salary_max:
            salary_str = f"{salary_min}" if salary_min else ""
            if salary_max:
                salary_str += f" - {salary_max}"
            st.write(f"**Зарплата:** {salary_str}")
        
        st.subheader("📊 Історія статусів")
        status_history = selected_response.get("status_history", [])
        
        if status_history:
            history_data = []
            for entry in status_history:
                history_data.append({
                    "Дата": entry.get("changed_at"),
                    "Від": entry.get("old_status"),
                    "До": entry.get("new_status"),
                    "Змінив": entry.get("changed_by", {}).get("fullname"),
                    "Коментар": entry.get("comment"),
                })
            
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.info("Історія статусів порожня")
        
        st.divider()
        st.subheader("✏️ Зміна статусу")
        
        new_status = st.selectbox(
            "Новий статус",
            options=["NEW", "INPROGRESS", "REJECTED", "AWAITING_DECISION", "PASSED_TO_MANAGER", "DOCUMENTATION", "INFORCE"],
            key=f"status_select_{selected_response.get('id')}"
        )
        
        comment = st.text_area("Коментар (опціонально)", key=f"comment_{selected_response.get('id')}")
        
        if st.button("💾 Оновити статус", key=f"save_status_{selected_response.get('id')}"):
            result = api._request(
                'PATCH',
                f'responses/{selected_response.get('id')}/status',
                json={
                    "new_status": new_status,
                    "comment": comment if comment else None
                }
            )
            
            if result:
                st.success("✅ Статус оновлено!")
                load_response_detail.clear()
                st.rerun()
            else:
                st.error("❌ Помилка при оновленні статусу")

else:
    st.info("👆 Виберіть відклик з таблиці для перегляду деталей")

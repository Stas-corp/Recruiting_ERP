from datetime import datetime

import pandas as pd
import streamlit as st

from utils.helpers import init_page
from utils.api_client import APIClient


init_page("Candidates", "👥")

st.header("👥 Candidates")

api = APIClient(token=st.session_state.get('token'))

@st.cache_data
def load_data():
    result = api._request('GET', 'candidates/')
    result.update(time_request=datetime.now().strftime("%H:%M %d.%m.%Y"))
    return result

api_response = load_data()

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Оновити таблицю"):
        load_data.clear()   # очищаем кэш
        st.toast("Таблиця оновлена!")
        api_response = load_data()
    st.metric("Всього кандидатів", api_response["total"])
# with col2:
#     st.metric("Показано", len(api_response["items"]))
with col2:
    st.metric("Завантажено", api_response["time_request"])    

# Преобразование данных для таблицы
table_data = []
for item in api_response["items"]:
    table_data.append({
        "ID": item["id"],
        "ФИО": item["full_name"],
        "Email": item["email"],
        "Телефон": item["phone"],
        "Должность": item["resume"],
        "Опыт": item["experience"],
        "Навыки": ", ".join(item["skills"]),
        "Примечания": item["notes"]
    })

df = pd.DataFrame(table_data)

# Отображение таблицы
st.dataframe(
    df,
    width="content",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="candidates_df",
    # column_config={
    #     "ID": st.column_config.NumberColumn("ID", width="small"),
    #     "ФИО": st.column_config.TextColumn("ФИО", width="medium"),
    #     "Email": st.column_config.TextColumn("Email", width="medium"),
    #     "Телефон": st.column_config.TextColumn("Телефон", width="medium"),
    #     # "Должность": st.column_config.TextColumn("Должность", width="medium"),
    #     # "Опыт": st.column_config.TextColumn("Опыт", width="medium"),
    #     # "Навыки": st.column_config.TextColumn("Навыки", width="large"),
    #     "Примечания": st.column_config.TextColumn("Примечания", width="medium"),
    # }
)

st.divider()

selected_rows = st.session_state["candidates_df"]["selection"]["rows"]

if selected_rows:
    selected_idx = selected_rows[0]
    selected_candidate = api_response["items"][selected_idx]
else:
    selected_candidate = api_response["items"][0]

col1, col2 = st.columns(2)
with col1:
    st.write(f"**ФИО:** {selected_candidate['full_name']}")
    st.write(f"**Email:** {selected_candidate['email']}")
    st.write(f"**Телефон:** {selected_candidate['phone']}")
with col2:
    st.write(f"**Резюме:** {selected_candidate['resume']}")
    st.write(f"**Опыт:** {selected_candidate['experience']}")

st.write("**Навыки:**")
skills_cols = st.columns(len(selected_candidate["skills"]))
for col, skill in zip(skills_cols, selected_candidate["skills"]):
    with col:
        st.info(skill)

st.write(f"**Примечания:** {selected_candidate['notes']}")

st.divider()

# Фильтрация по навыкам
st.subheader("🔍 Фильтр по навыкам")
all_skills = set()
for item in api_response["items"]:
    all_skills.update(item["skills"])

selected_skills = st.multiselect(
    "Выберите навыки",
    options=sorted(all_skills)
)

if selected_skills:
    filtered_candidates = [
        item for item in api_response["items"]
        if any(skill in item["skills"] for skill in selected_skills)
    ]
    st.write(f"**Найдено кандидатов: {len(filtered_candidates)}**")
    
    filtered_data = []
    for item in filtered_candidates:
        filtered_data.append({
            "ID": item["id"],
            "ФИО": item["full_name"],
            "Должность": item["resume"],
            "Совпадающие навыки": ", ".join([s for s in item["skills"] if s in selected_skills])
        })
    
    st.dataframe(pd.DataFrame(filtered_data), width="content", hide_index=True)
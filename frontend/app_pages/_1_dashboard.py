import streamlit as st
import pandas as pd
import plotly.express as px

from utils.helpers import init_page
from utils.api_client import APIClient


init_page("Main Page", "🏠")

st.header("🏠 Main Page")

api = APIClient(token=st.session_state.get('token'))

# KPI
col1, col2, col3, col4 = st.columns(4)

analytics = api._request('GET', 'analytics/overview')
if analytics:
    with col1:
        st.metric("Всього відгуків", analytics.get('total_responses', 0))
    # with col2:
    #     st.metric("Вакансій", analytics.get('total_vacancies', 0))
    # with col3:
    #     st.metric("Кандидатів", analytics.get('total_candidates', 0))
    # with col4:
    #     st.metric("Активные", analytics.get('active_vacancies', 0))

# Графики
st.subheader("Статистика")
col1, col2 = st.columns(2)

with col1:
    if analytics and 'status_breakdown' in analytics:
        status_data = analytics['status_breakdown']
        df = pd.DataFrame(status_data)
        fig = px.pie(df, values='count', names='status')
        st.plotly_chart(fig, width="content")

with col2:
    if analytics and 'source_breakdown' in analytics:
        source_data = analytics['source_breakdown']
        df = pd.DataFrame(source_data)
        fig = px.bar(df, x='source', y='count')
        st.plotly_chart(fig, width="content")
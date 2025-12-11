import requests
import streamlit as st
from typing import Optional, Dict, Any
from config import API_URL, API_TIMEOUT

class APIClient:
    def __init__(self, base_url: str = API_URL, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = requests.Session()
    
    def set_token(self, token: str):
        self.token = token
    
    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/v1/{endpoint}"
        kwargs.setdefault("timeout", API_TIMEOUT)
        kwargs.setdefault("headers", self._headers())
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            if response.status_code == 401:
                st.error("❌ Сесія закінчилася")
                st.session_state.token = None
                st.rerun()
            
            if response.status_code >= 400:
                st.error(f"❌ Помилка: {response.status_code}")
                return None
            
            return response.json() if response.content else {}
        except Exception as e:
            st.error(f"❌ Помилка підключення: {str(e)}")
            return None
    
    def login(self, email: str, password: str) -> Optional[Dict]:
        return self._request("POST", "auth/login", json={"email": email, "password": password})
    
    def register(self, email: str, password: str, full_name: str) -> Optional[Dict]:
        return self._request("POST", "auth/register",
                           json={"email": email, "password": password, "full_name": full_name})
    
    def get_candidates(self, skip: int = 0, limit: int = 100) -> Optional[Dict]:
        return self._request("GET", "candidates/", params={"skip": skip, "limit": limit})

api_client = APIClient()

from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from typing import Dict, Any

router = APIRouter()

@router.post("/sync-all")
async def sync_all_apis():
    return {"status": "sync started"}

@router.post("/work-ua")
async def receive_work_ua_response(data: Dict[str, Any]):
    return {"status": "received"}

@router.post("/robota-ua")
async def receive_robota_ua_response(data: Dict[str, Any]):
    return {"status": "received"}

@router.post("/olx")
async def receive_olx_response(data: Dict[str, Any]):
    return {"status": "received"}

@router.post("/website-form")
async def receive_website_form(data: Dict[str, Any]):
    return {"status": "received"}

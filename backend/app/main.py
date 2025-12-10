from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.session import engine
from app.db.models import Base, Role
from app.core.constants import RoleEnum
from app.db.session import SessionLocal
from app.api.v1 import auth, analytics, candidates, responses, users, vacancies, webhooks

Base.metadata.create_all(bind=engine)

db = SessionLocal()
if db.query(Role).count() == 0:
    roles = [
        Role(name=RoleEnum.ADMIN, description="Administrator", permissions=["*"]),
        Role(name=RoleEnum.RECRUITER, description="Recruiter", permissions=[
            "view_candidates", "edit_candidates",
            "view_responses", "change_response_status"
        ]),
        Role(name=RoleEnum.INTERVIEWER, description="Interviewer", permissions=[
            "view_candidates", "view_responses"
        ])
    ]
    db.add_all(roles)
    db.commit()
db.close()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты будут добавлены позже
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(candidates.router, prefix="/api/v1/candidates", tags=["candidates"])
app.include_router(responses.router, prefix="/api/v1/responses", tags=["responses"])
app.include_router(vacancies.router, prefix="/api/v1/vacancies", tags=["vacancies"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])

@app.get("/")
async def root():
    return {
        "message": "HR Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

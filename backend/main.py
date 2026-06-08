from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from database import engine

from database import Base

from routes.question_routes import router

from routes.execution_routes import router as execution_router

from routes.evaluation_routes import router as evaluation_router

from routes.interview_routes import router as interview_router

from models.submission_model import Submission

from models.company_question_model import CompanyQuestion

from models.resume_model import Resume

from routes.analytics_routes import (
    router as analytics_router
)

from routes.recommendation_routes import (
    router as recommendation_router
)

from routes.hint_routes import (
    router as hint_router
)

from models.session_model import InterviewSession

from routes.session_routes import (
    router as session_router
)

from models.user_model import User

from routes.user_routes import (
    router as user_router
)

from routes.resume_routes import router as resume_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(router)

app.include_router(execution_router)

app.include_router(evaluation_router)

app.include_router(interview_router)

app.include_router(analytics_router)

app.include_router(recommendation_router)

app.include_router(hint_router)

app.include_router(session_router)

app.include_router(user_router)

app.include_router(resume_router)

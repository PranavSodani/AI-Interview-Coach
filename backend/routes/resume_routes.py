from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db


from services.resume_service import (
    extract_text_from_pdf,
    save_resume,
    extract_resume_profile,
    get_starting_difficulty,
    get_latest_resume
)

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(
    user_id:int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    text = extract_text_from_pdf(contents)

    profile = extract_resume_profile(text)

    skills = profile.get("skills", [])

    print(profile)

    print(skills)

    resume_level = "Beginner"

    if len(profile.get("experience", [])) >= 2:
        resume_level = "Intermediate"

    if (
        len(profile.get("experience", [])) >= 2
        and
        len(profile.get("projects", [])) >= 2
    ):
        resume_level = "Advanced"

    profile["resume_level"] = resume_level

    starting_difficulty = (
        get_starting_difficulty(resume_level)
    )

    print(profile["resume_level"])

    print("Starting Difficulty:", starting_difficulty)

    resume = save_resume(
        user_id,
        file.filename,
        text,
        db
    )

    print(file.filename)

    print(len(contents))

    print(len(text))
    
    return {
        "resume_id": resume.id,
        "file_name": resume.file_name
    }

@router.get("/latest-resume")
def get_latest_resume_route(
    user_id: int,
    db: Session = Depends(get_db)
):
    resume = get_latest_resume(
        user_id,
        db
    )

    if not resume: 
        return None;

    return {
        "resume_id": resume.id,
        "file_name": resume.file_name
    }
from pydantic import BaseModel

class ResumeUploadResponse(BaseModel):

    id: int

    file_name: str
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from resume_generator import generate_resume
from models import ResumeData
from auth import verify_token

app = FastAPI(
    title="Resume Builder API",
    description="API for generating professional resumes with JWT authentication",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "Get your JWT token from jwt.io using the secret: ai_reume_anty_dolphin"
        },
        {
            "name": "Resume",
            "description": "Resume generation endpoints"
        }
    ]
)

# Security scheme for Swagger UI
security = HTTPBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[float] = None

class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str]

class Skill(BaseModel):
    category: str
    skills: List[str]

class ResumeData(BaseModel):
    template_name: Literal["ats_friendly", "modern_ats", "classic", "professional_ats", "modern_two_column"] = Field(
        description="Choose template style: ats_friendly, modern_ats, classic, professional_ats, or modern_two_column"
    )
    full_name: str
    profession: Optional[str] = None
    email: str
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill]

@app.get("/", tags=["Authentication"])
async def root():
    return {
        "message": "Welcome to Resume Builder API. Please include a valid JWT token in your requests.",
        "note": "Get your JWT token from jwt.io using the secret key from your .env file",
        "instructions": """
        1. Go to https://jwt.io
        2. In the payload section, add:
           {
             "sub": "your_user_id",
             "exp": 1735689600
           }
        3. In the "Verify Signature" section, enter the secret: ai_reume_anty_dolphin
        4. Copy the generated token from the encoded section
        5. Click the "Authorize" button in Swagger UI
        6. Enter the token as: Bearer <your_token>
        """
    }

@app.get("/templates", 
    tags=["Resume"],
    summary="Get available resume templates",
    description="Returns a list of all available resume templates and their descriptions. Requires JWT authentication.",
    dependencies=[Depends(verify_token)])
async def get_templates():
    return {
        "available_templates": [
            {
                "name": "modern_two_column",
                "description": "Modern two-column design with dark sidebar, icons, and professional styling"
            },
            {
                "name": "ats_friendly",
                "description": "Simple and clean ATS-friendly template optimized for applicant tracking systems"
            },
            {
                "name": "modern_ats",
                "description": "Modern design with colors while maintaining ATS compatibility"
            },
            {
                "name": "classic",
                "description": "Traditional black and white template with a timeless design"
            },
            {
                "name": "professional_ats",
                "description": "Professional template with subtle colors and ATS-friendly formatting"
            }
        ]
    }

@app.post("/generate-resume", 
    tags=["Resume"],
    summary="Generate a resume",
    description="Generates a PDF resume based on the provided data. Requires JWT authentication.",
    dependencies=[Depends(verify_token)])
async def create_resume(resume_data: ResumeData):
    try:
        file_path = generate_resume(resume_data)
        return {
            "message": "Resume generated successfully",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
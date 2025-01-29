# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import verify_token
from app.models.schemas import ResumeData
from app.services.resume_generator import generate_resume

router = APIRouter()

@router.get("/templates", 
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

@router.post("/generate", 
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
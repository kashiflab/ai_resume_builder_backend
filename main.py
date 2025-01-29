# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.endpoints import resume

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix=settings.API_V1_STR + "/resume", tags=["Resume"])

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
        3. In the "Verify Signature" section, enter the secret from your .env file
        4. Copy the generated token from the encoded section
        5. Use the token in your requests with the Authorization header:
           Bearer <your_token>
        """
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
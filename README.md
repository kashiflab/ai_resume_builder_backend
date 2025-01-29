# Resume Builder API

A FastAPI-based API that generates professional resumes in PDF format based on provided data. Secured with JWT authentication.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file with your JWT secret:
```bash
echo "JWT_SECRET=your_secret_key" > .env
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Authentication

All API endpoints (except `/` and `/token`) require JWT authentication. To use the API:

1. Get a JWT token:
```bash
curl -X POST http://localhost:8000/token
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
    "token_type": "bearer"
}
```

2. Include the token in subsequent requests:
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..." http://localhost:8000/templates
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Templates

The API supports multiple resume templates, each designed for different purposes:

### 1. Modern Two-Column (`modern_two_column`)
A contemporary design featuring:
- Professional dark sidebar with white text
- Two-column layout for optimal space usage
- Left sidebar containing:
  - Name and contact information
  - Skills section with categorized skills
- Main content area with:
  - Professional summary
  - Work experience with bullet points
  - Education details
- Modern typography using Helvetica font family
- Professional color scheme:
  - Dark blue sidebar (#34495e)
  - Dark grey text (#2c3e50)
  - Light grey dates (#7f8c8d)
- Perfect for creative professionals and modern industries

### 2. ATS Friendly (`ats_friendly`)
- Simple and clean design
- Optimized for Applicant Tracking Systems
- Black and white color scheme
- Maximum text parsing compatibility
- Recommended for corporate job applications

### 3. Modern ATS (`modern_ats`)
- Modern design with professional colors
- ATS-compatible formatting
- Subtle borders and styling
- Blue color scheme
- Good balance between style and ATS compatibility

### 4. Classic (`classic`)
- Traditional black and white template
- Timeless design
- Centered headers
- Justified text alignment
- Perfect for academic and traditional industries

### 5. Professional ATS (`professional_ats`)
- Professional design with subtle colors
- ATS-friendly formatting
- Light grey section backgrounds
- Navy blue accents
- Ideal for business professionals

You can view available templates and their descriptions by sending a GET request to `/templates`.

## API Endpoints

### GET /
- Welcome message
- No authentication required
- Returns: `{"message": "Welcome to Resume Builder API. Please authenticate to use the services."}`

### POST /token
- Get JWT authentication token
- No authentication required
- Returns: JWT token for authentication

### GET /templates
- Lists all available resume templates with descriptions
- Requires JWT authentication
- Returns: List of templates with names and descriptions

### POST /generate-resume
Generates a PDF resume based on the provided data.
- Requires JWT authentication

Example request:
```bash
curl -X POST http://localhost:8000/generate-resume \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "template_name": "modern_two_column",
    "full_name": "Frank Graham",
    "profession": "Senior Software Engineer",
    "email": "frank.graham@example.com",
    "phone": "+1 234 567 8900",
    "linkedin": "linkedin.com/in/frankgraham",
    "summary": "Senior Software Engineer with over 8 years of experience...",
    "education": [
        {
            "institution": "University of Technology",
            "degree": "Master of Science",
            "field_of_study": "Computer Science",
            "start_date": "2018",
            "end_date": "2020",
            "gpa": 3.9
        }
    ],
    "experience": [
        {
            "company": "Tech Innovations Inc.",
            "position": "Senior Software Engineer",
            "start_date": "2020-06",
            "end_date": "Present",
            "description": [
                "Led development of cloud-native microservices architecture",
                "Managed team of 6 developers across multiple projects"
            ]
        }
    ],
    "skills": [
        {
            "category": "Programming",
            "skills": ["Python", "JavaScript", "Java"]
        }
    ]
}'
```

Response:
```json
{
    "message": "Resume generated successfully",
    "file_path": "generated_resumes/Frank_Graham_20240128_123456.pdf"
}
```

## Generated Files
- The generated PDF resumes will be stored in the `generated_resumes` directory
- Each file is named using the format: `{full_name}_{timestamp}.pdf`
- Files are automatically created with unique timestamps to prevent overwrites

## Template Selection Tips
1. For corporate job applications, use `ats_friendly` or `professional_ats`
2. For creative or modern industries, use `modern_two_column`
3. For academic positions, use `classic`
4. For a balance between modern design and ATS compatibility, use `modern_ats`

## Security Notes
1. In production, replace the JWT secret with a strong, unique key
2. Consider implementing proper user authentication before issuing tokens
3. Use HTTPS in production
4. Implement rate limiting for token generation and API endpoints
5. Consider adding token expiration and refresh token functionality 
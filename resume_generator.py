from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from datetime import datetime
import os
from resume_templates import get_template
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_contact_line(icon_type, text, style):
    """
    Creates a line of contact information with a Unicode symbol.
    
    Args:
        icon_type (str): Type of contact info ('email', 'phone', or 'linkedin')
        text (str): Contact information text
        style (ParagraphStyle): Style for the text
    
    Returns:
        list: A list containing the symbol and text for use in a Table
    """
    # Unicode symbols for different contact types
    icons = {
        'email': '✉',
        'phone': '☎',
        'linkedin': '🔗',
        'default': '•'
    }
    
    icon_style = ParagraphStyle(
        'Icon',
        parent=style,
        fontSize=style.fontSize + 2,
        textColor=style.textColor,
        leading=style.leading
    )
    
    icon_symbol = icons.get(icon_type, icons['default'])
    return [[Paragraph(icon_symbol, icon_style), Paragraph(text, style)]]

def generate_resume(resume_data):
    # Create icons directory if it doesn't exist
    icons_dir = "icons"
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
        
    # Create default icons if they don't exist (you can replace these with your own icons)
    default_icons = {
        'email': '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="18px" height="18px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
        </svg>
        ''',
        'phone': '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="18px" height="18px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
        </svg>
        ''',
        'linkedin': '''
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" width="18px" height="18px">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/>
        </svg>
        '''
    }

    for icon_name, svg_content in default_icons.items():
        icon_path = os.path.join(icons_dir, f"{icon_name}.png")
        if not os.path.exists(icon_path):
            convert_svg_to_png(svg_content, icon_path)

    # Create output directory if it doesn't exist
    output_dir = "generated_resumes"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{resume_data.full_name.replace(' ', '_')}_{timestamp}.pdf"

    # Create the PDF document with adjusted margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    # Get the selected template
    template = get_template(resume_data.template_name)
    styles = template.get_styles()

    if template.get_template_type() == "two_column":
        return generate_two_column_resume(doc, resume_data, styles)
    else:
        return generate_single_column_resume(doc, resume_data, styles)

def generate_single_column_resume(doc, resume_data, styles):
    content = []

    # Header
    content.append(Paragraph(resume_data.full_name, styles['title']))
    contact_info = []
    if resume_data.email:
        contact_info.append(resume_data.email)
    if resume_data.phone:
        contact_info.append(resume_data.phone)
    if resume_data.linkedin:
        contact_info.append(resume_data.linkedin)
    content.append(Paragraph(" | ".join(contact_info), styles['normal']))
    content.append(Spacer(1, 20))

    # Summary
    content.append(Paragraph("Professional Summary", styles['heading']))
    content.append(Paragraph(resume_data.summary, styles['normal']))
    content.append(Spacer(1, 20))

    # Experience
    content.append(Paragraph("Professional Experience", styles['heading']))
    for exp in resume_data.experience:
        company_line = f"<b>{exp.company}</b> - {exp.position}"
        date_line = f"{exp.start_date} - {exp.end_date if exp.end_date else 'Present'}"
        content.append(Paragraph(company_line, styles['normal']))
        content.append(Paragraph(date_line, styles['normal']))
        for desc in exp.description:
            content.append(Paragraph(f"• {desc}", styles['normal']))
        content.append(Spacer(1, 12))

    # Education
    content.append(Paragraph("Education", styles['heading']))
    for edu in resume_data.education:
        edu_line = f"<b>{edu.institution}</b>"
        degree_line = f"{edu.degree} in {edu.field_of_study}"
        date_line = f"{edu.start_date} - {edu.end_date if edu.end_date else 'Present'}"
        if edu.gpa:
            degree_line += f" (GPA: {edu.gpa})"
        content.append(Paragraph(edu_line, styles['normal']))
        content.append(Paragraph(degree_line, styles['normal']))
        content.append(Paragraph(date_line, styles['normal']))
        content.append(Spacer(1, 12))

    # Skills
    content.append(Paragraph("Skills", styles['heading']))
    for skill in resume_data.skills:
        skill_line = f"<b>{skill.category}:</b> {', '.join(skill.skills)}"
        content.append(Paragraph(skill_line, styles['normal']))
        content.append(Spacer(1, 6))

    # Build the PDF
    doc.build(content)
    return doc.filename

def generate_two_column_resume(doc, resume_data, styles):
    # Calculate column widths with adjusted margins
    page_width = letter[0] - doc.leftMargin - doc.rightMargin
    sidebar_width = page_width * 0.32  # Slightly wider sidebar
    main_width = page_width * 0.68     # Adjusted main content

    # Prepare sidebar content (left column)
    sidebar_content = []
    
    # Add some top spacing
    sidebar_content.append(Spacer(1, 20))
    
    # Personal Info in sidebar
    sidebar_content.append(Paragraph(resume_data.full_name.upper(), styles['title']))
    # Add job title/profession
    if hasattr(resume_data, 'profession'):
        sidebar_content.append(Paragraph(resume_data.profession.upper(), styles['subtitle']))
    else:
        # Extract profession from the most recent job
        if resume_data.experience:
            sidebar_content.append(Paragraph(resume_data.experience[0].position.upper(), styles['subtitle']))

    sidebar_content.append(Spacer(1, 20))

    # Contact Information with icons
    sidebar_content.append(Paragraph("CONTACT", styles['sidebar_heading']))
    sidebar_content.append(Spacer(1, 8))
    
    # Email
    if resume_data.email:
        email_table = Table(
            create_contact_line("email", resume_data.email, styles['contact']),
            colWidths=[12, sidebar_width-45],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ])
        )
        sidebar_content.append(email_table)

    # Phone
    if resume_data.phone:
        phone_table = Table(
            create_contact_line("phone", resume_data.phone, styles['contact']),
            colWidths=[12, sidebar_width-45],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ])
        )
        sidebar_content.append(phone_table)

    # LinkedIn
    if resume_data.linkedin:
        linkedin_table = Table(
            create_contact_line("linkedin", resume_data.linkedin, styles['contact']),
            colWidths=[12, sidebar_width-45],
            style=TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ])
        )
        sidebar_content.append(linkedin_table)

    sidebar_content.append(Spacer(1, 25))

    # Skills in sidebar
    sidebar_content.append(Paragraph("EXPERTISE", styles['sidebar_heading']))
    sidebar_content.append(Spacer(1, 10))
    for skill in resume_data.skills:
        sidebar_content.append(Paragraph(skill.category.upper(), styles['skill_category']))
        # Create skill bars or bullet points
        for s in skill.skills:
            sidebar_content.append(Paragraph(f"• {s}", styles['skill_level']))
        sidebar_content.append(Spacer(1, 6))

    # Prepare main content (right column)
    main_content = []
    main_content.append(Spacer(1, 20))

    # Summary in main content
    main_content.append(Paragraph("ABOUT ME", styles['main_heading']))
    main_content.append(Spacer(1, 8))
    main_content.append(Paragraph(resume_data.summary, styles['main_normal']))
    main_content.append(Spacer(1, 25))

    # Experience in main content
    main_content.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['main_heading']))
    main_content.append(Spacer(1, 8))
    for exp in resume_data.experience:
        main_content.append(Paragraph(exp.position.upper(), styles['job_title']))
        main_content.append(Paragraph(exp.company, styles['company']))
        main_content.append(Paragraph(
            f"{exp.start_date} - {exp.end_date if exp.end_date else 'Present'}", 
            styles['date']
        ))
        for desc in exp.description:
            main_content.append(Paragraph(f"• {desc}", styles['main_normal']))
        main_content.append(Spacer(1, 15))

    # Education in main content
    main_content.append(Paragraph("EDUCATION", styles['main_heading']))
    main_content.append(Spacer(1, 8))
    for edu in resume_data.education:
        main_content.append(Paragraph(f"{edu.degree} in {edu.field_of_study}".upper(), styles['job_title']))
        main_content.append(Paragraph(edu.institution, styles['company']))
        date_text = f"{edu.start_date} - {edu.end_date if edu.end_date else 'Present'}"
        if edu.gpa:
            date_text += f" | GPA: {edu.gpa}"
        main_content.append(Paragraph(date_text, styles['date']))
        main_content.append(Spacer(1, 12))

    # Create sidebar table with background
    sidebar_table = Table(
        [[para] for para in sidebar_content],
        colWidths=[sidebar_width],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),  # Darker blue background
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    )

    # Create main content table
    main_table = Table(
        [[para] for para in main_content],
        colWidths=[main_width],
        style=TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 25),
            ('RIGHTPADDING', (0, 0), (-1, -1), 25),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    )

    # Create the main table that holds both columns
    main_table = Table(
        [[sidebar_table, main_table]],
        colWidths=[sidebar_width, main_width],
        style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ])
    )

    # Build the PDF with error handling
    try:
        doc.build([main_table])
    except:
        # If the content is too large, try with smaller font sizes
        new_styles = get_template(resume_data.template_name).get_styles(scale_factor=0.9)
        return generate_two_column_resume(doc, resume_data, new_styles)
    
    return doc.filename 
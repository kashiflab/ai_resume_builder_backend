# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch
from datetime import datetime
import os
from .resume_templates import get_template
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
    if resume_data.profession:
        sidebar_content.append(Paragraph(resume_data.profession.upper(), styles['subtitle']))
    elif resume_data.experience:
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
    main_content.append(Spacer(1, 20))

    # Experience in main content
    main_content.append(Paragraph("EXPERIENCE", styles['main_heading']))
    main_content.append(Spacer(1, 8))
    for exp in resume_data.experience:
        main_content.append(Paragraph(exp.position.upper(), styles['main_subheading']))
        main_content.append(Paragraph(f"{exp.company} | {exp.start_date} - {exp.end_date if exp.end_date else 'Present'}", styles['main_normal']))
        for desc in exp.description:
            main_content.append(Paragraph(f"• {desc}", styles['main_normal']))
        main_content.append(Spacer(1, 12))

    # Education in main content
    main_content.append(Paragraph("EDUCATION", styles['main_heading']))
    main_content.append(Spacer(1, 8))
    for edu in resume_data.education:
        main_content.append(Paragraph(edu.institution.upper(), styles['main_subheading']))
        degree_line = f"{edu.degree} in {edu.field_of_study}"
        if edu.gpa:
            degree_line += f" (GPA: {edu.gpa})"
        main_content.append(Paragraph(degree_line, styles['main_normal']))
        main_content.append(Paragraph(f"{edu.start_date} - {edu.end_date if edu.end_date else 'Present'}", styles['main_normal']))
        main_content.append(Spacer(1, 12))

    # Create the two-column layout
    table_data = [[Table(sidebar_content, colWidths=[sidebar_width]), Table(main_content, colWidths=[main_width])]]
    table = Table(table_data, colWidths=[sidebar_width, main_width])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    # Build the PDF
    doc.build([table])
    return doc.filename 
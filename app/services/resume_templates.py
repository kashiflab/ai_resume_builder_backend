# -*- coding: utf-8 -*-
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Frame, Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class ResumeTemplate:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        
    def get_styles(self):
        raise NotImplementedError
        
    def get_template_type(self):
        return "single_column"

class ModernTwoColumnTemplate(ResumeTemplate):
    def get_template_type(self):
        return "two_column"
        
    def get_styles(self, scale_factor=1.0):
        # Modern two-column template with elegant styling
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=int(26 * scale_factor),
            spaceAfter=int(2 * scale_factor),
            textColor=colors.white,
            alignment=TA_LEFT,
            leading=int(32 * scale_factor),
            fontName='Helvetica-Bold',
            letterSpacing=1
        )

        subtitle_style = ParagraphStyle(
            'SubTitle',
            parent=self.styles['Normal'],
            fontSize=int(12 * scale_factor),
            textColor=colors.HexColor('#E8E8E8'),
            alignment=TA_LEFT,
            leading=int(14 * scale_factor),
            spaceAfter=int(25 * scale_factor),
            fontName='Helvetica',
            letterSpacing=0.5
        )
        
        sidebar_heading_style = ParagraphStyle(
            'SidebarHeading',
            parent=self.styles['Heading2'],
            fontSize=int(13 * scale_factor),
            spaceAfter=int(10 * scale_factor),
            textColor=colors.HexColor('#4FC3F7'),
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            leading=int(15 * scale_factor),
            letterSpacing=1
        )
        
        sidebar_normal_style = ParagraphStyle(
            'SidebarNormal',
            parent=self.styles['Normal'],
            fontSize=int(9 * scale_factor),
            textColor=colors.white,
            spaceAfter=int(4 * scale_factor),
            alignment=TA_LEFT,
            leading=int(11 * scale_factor),
            fontName='Helvetica-Light'
        )

        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=self.styles['Normal'],
            fontSize=int(9 * scale_factor),
            textColor=colors.HexColor('#E0E0E0'),
            spaceAfter=int(4 * scale_factor),
            alignment=TA_LEFT,
            leading=int(11 * scale_factor),
            leftIndent=int(20 * scale_factor),
            fontName='Helvetica-Light'
        )
        
        main_heading_style = ParagraphStyle(
            'MainHeading',
            parent=self.styles['Heading2'],
            fontSize=int(16 * scale_factor),
            spaceAfter=int(12 * scale_factor),
            textColor=colors.HexColor('#1976D2'),
            spaceBefore=int(12 * scale_factor),
            fontName='Helvetica-Bold',
            leading=int(18 * scale_factor),
            letterSpacing=0.8
        )
        
        main_normal_style = ParagraphStyle(
            'MainNormal',
            parent=self.styles['Normal'],
            fontSize=int(10 * scale_factor),
            textColor=colors.HexColor('#424242'),
            spaceAfter=int(6 * scale_factor),
            leading=int(14 * scale_factor),
            fontName='Helvetica',
            alignment=TA_JUSTIFY
        )

        main_subheading_style = ParagraphStyle(
            'MainSubheading',
            parent=self.styles['Normal'],
            fontSize=int(12 * scale_factor),
            textColor=colors.HexColor('#1976D2'),
            spaceAfter=int(2 * scale_factor),
            fontName='Helvetica-Bold',
            leading=int(14 * scale_factor),
            letterSpacing=0.5
        )
        
        skill_category_style = ParagraphStyle(
            'SkillCategory',
            parent=self.styles['Normal'],
            fontSize=int(10 * scale_factor),
            textColor=colors.HexColor('#4FC3F7'),
            alignment=TA_LEFT,
            fontName='Helvetica-Bold',
            spaceBefore=int(8 * scale_factor),
            leading=int(12 * scale_factor),
            letterSpacing=0.5
        )

        skill_level_style = ParagraphStyle(
            'SkillLevel',
            parent=self.styles['Normal'],
            fontSize=int(9 * scale_factor),
            textColor=colors.HexColor('#E0E0E0'),
            alignment=TA_LEFT,
            spaceAfter=int(2 * scale_factor),
            leading=int(11 * scale_factor),
            fontName='Helvetica-Light',
            leftIndent=10
        )
        
        return {
            'title': title_style,
            'subtitle': subtitle_style,
            'sidebar_heading': sidebar_heading_style,
            'sidebar_normal': sidebar_normal_style,
            'contact': contact_style,
            'main_heading': main_heading_style,
            'main_normal': main_normal_style,
            'main_subheading': main_subheading_style,
            'skill_category': skill_category_style,
            'skill_level': skill_level_style
        }

class ATSFriendlyTemplate(ResumeTemplate):
    def get_styles(self):
        # Simple, clean styles optimized for ATS
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.black
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.black,
            spaceBefore=15
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6
        )
        
        return {
            'title': title_style,
            'heading': heading_style,
            'normal': normal_style
        }

class ModernATSTemplate(ResumeTemplate):
    def get_styles(self):
        # Modern styles with colors while maintaining ATS compatibility
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor('#0d47a1'),
            spaceBefore=15,
            borderColor=colors.HexColor('#1a237e'),
            borderWidth=1,
            borderPadding=5
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            spaceAfter=8
        )
        
        return {
            'title': title_style,
            'heading': heading_style,
            'normal': normal_style
        }

class ClassicTemplate(ResumeTemplate):
    def get_styles(self):
        # Traditional black and white template
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.black,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=10,
            textColor=colors.black,
            spaceBefore=15,
            borderWidth=0.5,
            borderPadding=5,
            borderColor=colors.black
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6
        )
        
        return {
            'title': title_style,
            'heading': heading_style,
            'normal': normal_style
        }

class ProfessionalATSTemplate(ResumeTemplate):
    def get_styles(self):
        # Professional template with subtle colors
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            textColor=colors.HexColor('#2c3e50'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=13,
            spaceAfter=10,
            textColor=colors.HexColor('#34495e'),
            spaceBefore=15,
            borderColor=colors.HexColor('#bdc3c7'),
            borderWidth=0.5,
            borderPadding=5
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6
        )
        
        return {
            'title': title_style,
            'heading': heading_style,
            'normal': normal_style
        }

def get_template(template_name: str) -> ResumeTemplate:
    """
    Factory function to get the appropriate resume template
    """
    templates = {
        'modern_two_column': ModernTwoColumnTemplate(),
        'ats_friendly': ATSFriendlyTemplate(),
        'modern_ats': ModernATSTemplate(),
        'classic': ClassicTemplate(),
        'professional_ats': ProfessionalATSTemplate()
    }
    
    return templates.get(template_name, ATSFriendlyTemplate()) 
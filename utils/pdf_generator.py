"""
AI Investigation Report Generator - Premium PDF Report System
Generates comprehensive, professional PDF reports with fraud analysis, evidence, and risk factors.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import os
from pathlib import Path


def generate_investigation_report(claim, app_config):
    """
    Generate a comprehensive AI Investigation Report PDF
    
    Args:
        claim: SQLite Row object containing claim data
        app_config: Flask app config with UPLOAD_FOLDER path
    
    Returns:
        BytesIO buffer containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for PDF elements
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1d4ed8'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=34
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=20,
        fontName='Helvetica-Bold',
        leading=22
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1d4ed8'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        leading=20,
        borderWidth=1,
        borderColor=colors.HexColor('#e5e7eb'),
        borderPadding=8,
        backColor=colors.HexColor('#f3f6fb')
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        leading=14,
        alignment=TA_JUSTIFY
    )
    
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#1d4ed8'),
        fontName='Helvetica-Bold',
        spaceAfter=8
    )
    
    risk_high_style = ParagraphStyle(
        'RiskHigh',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#dc2626'),
        fontName='Helvetica-Bold',
        spaceAfter=8
    )
    
    risk_low_style = ParagraphStyle(
        'RiskLow',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#10b981'),
        fontName='Helvetica-Bold',
        spaceAfter=8
    )
    
    # ========== COVER PAGE ==========
    story.append(Spacer(1, 1.5*inch))
    
    # Title
    title_text = f"<b>AI INVESTIGATION REPORT</b><br/><br/>Claim Analysis & Fraud Detection"
    story.append(Paragraph(title_text, title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Report ID and Date
    report_id = f"Report ID: CW-{claim['id']:06d}"
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    story.append(Paragraph(f"<b>{report_id}</b>", highlight_style))
    story.append(Paragraph(f"Generated: {report_date}", body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Status Badge
    if claim['prediction_label'] == 'Fraud':
        status_color = '#dc2626'
        status_text = "⚠️ HIGH RISK - FRAUD DETECTED"
    else:
        status_color = '#10b981'
        status_text = "✅ LOW RISK - LEGITIMATE CLAIM"
    
    status_style = ParagraphStyle(
        'Status',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.HexColor(status_color),
        fontName='Helvetica-Bold',
        alignment=TA_CENTER,
        spaceAfter=20,
        backColor=colors.HexColor('#f3f6fb'),
        borderWidth=2,
        borderColor=colors.HexColor(status_color),
        borderPadding=15
    )
    story.append(Paragraph(status_text, status_style))
    
    story.append(PageBreak())
    
    # ========== EXECUTIVE SUMMARY ==========
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    
    fraud_score = claim['prediction_score'] * 100
    summary_text = f"""
    This comprehensive AI-powered investigation report analyzes claim #{claim['id']} submitted by 
    <b>{claim['claimant_name']}</b>. The advanced machine learning fraud detection system has evaluated 
    multiple risk factors and determined a fraud probability score of <b>{fraud_score:.2f}%</b>.
    
    <br/><br/>
    
    <b>Claim Details:</b><br/>
    • Claim Type: {claim['claim_type']}<br/>
    • Claim Amount: ${claim['claim_amount']:,.2f}<br/>
    • Incident Date: {claim['incident_date']}<br/>
    • Policy Age: {claim['age_of_policy_days']} days<br/>
    • Previous Claims: {claim['number_of_previous_claims']}<br/>
    
    <br/>
    
    <b>AI Assessment:</b><br/>
    The system has classified this claim as <b>{claim['prediction_label']}</b> based on comprehensive 
    analysis of historical patterns, behavioral indicators, and risk factors. This report provides 
    detailed evidence, risk factor analysis, and recommendations for further action.
    """
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # ========== FRAUD SCORE VISUALIZATION ==========
    story.append(Paragraph("FRAUD RISK SCORE", heading_style))
    
    # Create a visual representation of the fraud score
    score_data = [
        ['Risk Category', 'Score', 'Status'],
        ['Fraud Probability', f"{fraud_score:.2f}%", claim['prediction_label']],
        ['Confidence Level', f"{(1 - abs(fraud_score/100 - (1 if claim['prediction_label'] == 'Fraud' else 0))) * 100:.1f}%", 'High'],
    ]
    
    score_table = Table(score_data, colWidths=[3*inch, 2*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4ed8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f6fb')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dbe3f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f9fe')]),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Risk level explanation
    if fraud_score >= 80:
        risk_explanation = f"""
        <b>CRITICAL RISK LEVEL:</b> This claim exhibits extremely high fraud indicators. Multiple 
        risk factors align with known fraudulent patterns. Immediate investigation and verification 
        of all submitted documentation is strongly recommended.
        """
        story.append(Paragraph(risk_explanation, risk_high_style))
    elif fraud_score >= 60:
        risk_explanation = f"""
        <b>HIGH RISK LEVEL:</b> This claim shows significant fraud indicators. Several risk factors 
        suggest potential fraudulent activity. Thorough review and additional verification steps 
        are recommended.
        """
        story.append(Paragraph(risk_explanation, risk_high_style))
    elif fraud_score >= 40:
        risk_explanation = f"""
        <b>MODERATE RISK LEVEL:</b> This claim displays some concerning patterns that warrant 
        additional scrutiny. Standard verification procedures should be followed with extra attention 
        to detail.
        """
        story.append(Paragraph(risk_explanation, highlight_style))
    else:
        risk_explanation = f"""
        <b>LOW RISK LEVEL:</b> This claim appears legitimate based on AI analysis. Risk factors 
        are within acceptable ranges. Standard processing procedures can be followed.
        """
        story.append(Paragraph(risk_explanation, risk_low_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ========== RISK FACTORS ANALYSIS ==========
    story.append(Paragraph("DETAILED RISK FACTORS ANALYSIS", heading_style))
    
    # Calculate individual risk contributions
    risk_factors = []
    
    # Policy Age Risk
    policy_age = claim['age_of_policy_days']
    if policy_age < 30:
        policy_risk = "HIGH"
        policy_score = 0.3
        policy_note = "Very new policy increases fraud risk"
    elif policy_age < 90:
        policy_risk = "MEDIUM"
        policy_score = 0.15
        policy_note = "Recent policy requires attention"
    elif policy_age < 180:
        policy_risk = "LOW-MEDIUM"
        policy_score = 0.1
        policy_note = "Young policy, moderate risk"
    else:
        policy_risk = "LOW"
        policy_score = 0.05
        policy_note = "Established policy, lower risk"
    
    risk_factors.append([
        'Policy Age',
        f"{policy_age} days",
        policy_risk,
        f"{policy_score*100:.0f}%",
        policy_note
    ])
    
    # Previous Claims Risk
    prev_claims = claim['number_of_previous_claims']
    if prev_claims >= 5:
        prev_risk = "HIGH"
        prev_score = 0.25
        prev_note = "Excessive claim history indicates pattern"
    elif prev_claims >= 3:
        prev_risk = "MEDIUM"
        prev_score = 0.15
        prev_note = "Multiple previous claims raise concern"
    elif prev_claims >= 1:
        prev_risk = "LOW-MEDIUM"
        prev_score = 0.08
        prev_note = "Some claim history present"
    else:
        prev_risk = "LOW"
        prev_score = 0.02
        prev_note = "No previous claims, positive indicator"
    
    risk_factors.append([
        'Previous Claims',
        str(prev_claims),
        prev_risk,
        f"{prev_score*100:.0f}%",
        prev_note
    ])
    
    # Location Risk
    loc_risk_score = claim['location_risk_score']
    if loc_risk_score >= 0.7:
        loc_risk = "HIGH"
        loc_score = 0.2
        loc_note = "High-risk geographic area"
    elif loc_risk_score >= 0.5:
        loc_risk = "MEDIUM"
        loc_score = 0.12
        loc_note = "Moderate-risk location"
    elif loc_risk_score >= 0.3:
        loc_risk = "LOW-MEDIUM"
        loc_score = 0.06
        loc_note = "Average risk location"
    else:
        loc_risk = "LOW"
        loc_score = 0.03
        loc_note = "Low-risk geographic area"
    
    risk_factors.append([
        'Location Risk',
        f"{loc_risk_score:.2f}",
        loc_risk,
        f"{loc_score*100:.0f}%",
        loc_note
    ])
    
    # Claim Amount Risk
    claim_amount = claim['claim_amount']
    if claim_amount >= 50000:
        amount_risk = "HIGH"
        amount_score = 0.15
        amount_note = "Very high claim amount increases risk"
    elif claim_amount >= 20000:
        amount_risk = "MEDIUM"
        amount_score = 0.1
        amount_note = "High claim amount requires scrutiny"
    elif claim_amount >= 10000:
        amount_risk = "LOW-MEDIUM"
        amount_score = 0.05
        amount_note = "Moderate claim amount"
    else:
        amount_risk = "LOW"
        amount_score = 0.02
        amount_note = "Lower claim amount, reduced risk"
    
    risk_factors.append([
        'Claim Amount',
        f"${claim_amount:,.2f}",
        amount_risk,
        f"{amount_score*100:.0f}%",
        amount_note
    ])
    
    # Police Report
    if claim['police_report_filed']:
        police_risk = "LOW"
        police_score = -0.1
        police_note = "Police report filed, reduces risk"
    else:
        police_risk = "MEDIUM"
        police_score = 0.1
        police_note = "No police report, increases suspicion"
    
    risk_factors.append([
        'Police Report',
        "Yes" if claim['police_report_filed'] else "No",
        police_risk,
        f"{police_score*100:+.0f}%",
        police_note
    ])
    
    # Witnesses
    witnesses = claim['witnesses']
    if witnesses >= 3:
        witness_risk = "LOW"
        witness_score = -0.08
        witness_note = "Multiple witnesses support legitimacy"
    elif witnesses >= 1:
        witness_risk = "LOW-MEDIUM"
        witness_score = -0.04
        witness_note = "Witnesses present, positive indicator"
    else:
        witness_risk = "MEDIUM"
        witness_score = 0.08
        witness_note = "No witnesses, increases risk"
    
    risk_factors.append([
        'Witnesses',
        str(witnesses),
        witness_risk,
        f"{witness_score*100:+.0f}%",
        witness_note
    ])
    
    # Risk Factors Table
    risk_table_data = [['Risk Factor', 'Value', 'Risk Level', 'Impact', 'Analysis']]
    risk_table_data.extend(risk_factors)
    
    risk_table = Table(risk_table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 0.8*inch, 2.2*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4ed8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dbe3f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f9fe')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 0.3*inch))
    
    # ========== CLAIMANT INFORMATION ==========
    story.append(Paragraph("CLAIMANT INFORMATION", heading_style))
    
    claimant_data = [
        ['Field', 'Value'],
        ['Name', claim['claimant_name']],
        ['Email', claim['claimant_email']],
        ['Age', str(claim['claimant_age']) if claim['claimant_age'] else 'N/A'],
        ['Gender', claim['claimant_gender'] if claim['claimant_gender'] else 'N/A'],
        ['Claim Type', claim['claim_type']],
        ['Incident Date', claim['incident_date']],
        ['Claim Amount', f"${claim['claim_amount']:,.2f}"],
        ['Submitted Date', claim['created_at']],
    ]
    
    if claim.get('police_report_number'):
        claimant_data.append(['Police Report #', claim['police_report_number']])
    
    claimant_table = Table(claimant_data, colWidths=[2.5*inch, 4.5*inch])
    claimant_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4ed8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f6fb')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dbe3f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f9fe')]),
    ]))
    story.append(claimant_table)
    story.append(Spacer(1, 0.3*inch))
    
    # ========== EVIDENCE SECTION ==========
    if claim.get('claim_image'):
        story.append(Paragraph("EVIDENCE & DOCUMENTATION", heading_style))
        
        image_path = os.path.join(app_config['UPLOAD_FOLDER'], claim['claim_image'])
        if os.path.exists(image_path):
            try:
                # Add image to PDF
                img = Image(image_path, width=5*inch, height=3.75*inch)
                story.append(img)
                story.append(Spacer(1, 0.2*inch))
                story.append(Paragraph(f"<i>Evidence Image: {claim['claim_image']}</i>", 
                                     ParagraphStyle('ImageCaption', parent=styles['Normal'], 
                                                   fontSize=9, textColor=colors.HexColor('#6b7280'),
                                                   alignment=TA_CENTER)))
            except Exception as e:
                story.append(Paragraph(f"<i>Evidence image available but could not be embedded: {str(e)}</i>", 
                                     body_style))
        else:
            story.append(Paragraph("<i>Evidence image referenced but file not found.</i>", body_style))
        
        story.append(Spacer(1, 0.3*inch))
    
    # Description if available
    if claim.get('description'):
        story.append(Paragraph("INCIDENT DESCRIPTION", heading_style))
        desc_text = claim['description'].replace('\n', '<br/>')
        story.append(Paragraph(desc_text, body_style))
        story.append(Spacer(1, 0.3*inch))
    
    # ========== AI INSIGHTS & RECOMMENDATIONS ==========
    story.append(Paragraph("AI INSIGHTS & RECOMMENDATIONS", heading_style))
    
    if claim['prediction_label'] == 'Fraud':
        insights_text = f"""
        <b>Fraud Detection Analysis:</b><br/><br/>
        
        Based on comprehensive machine learning analysis, this claim has been flagged as potentially 
        fraudulent with a confidence score of {fraud_score:.2f}%. The AI system has identified multiple 
        risk indicators that align with known fraudulent patterns:<br/><br/>
        
        • <b>Policy Age Risk:</b> {policy_note}<br/>
        • <b>Claim History:</b> {prev_note}<br/>
        • <b>Geographic Risk:</b> {loc_note}<br/>
        • <b>Amount Analysis:</b> {amount_note}<br/>
        • <b>Documentation:</b> {police_note}<br/>
        • <b>Witness Verification:</b> {witness_note}<br/><br/>
        
        <b>Recommended Actions:</b><br/>
        1. Conduct thorough manual review of all submitted documentation<br/>
        2. Verify claimant identity and contact information<br/>
        3. Cross-reference with previous claims database<br/>
        4. Contact relevant authorities if police report was filed<br/>
        5. Request additional supporting documentation<br/>
        6. Consider flagging for enhanced monitoring<br/><br/>
        
        <b>Next Steps:</b> This claim requires immediate attention from the fraud investigation team. 
        All evidence should be preserved and a detailed case file should be created for potential 
        legal proceedings.
        """
    else:
        insights_text = f"""
        <b>Legitimacy Assessment:</b><br/><br/>
        
        The AI analysis indicates this claim appears legitimate with a fraud probability of 
        {fraud_score:.2f}%. The risk factors evaluated suggest normal claim patterns:<br/><br/>
        
        • <b>Policy Age:</b> {policy_note}<br/>
        • <b>Claim History:</b> {prev_note}<br/>
        • <b>Geographic Risk:</b> {loc_note}<br/>
        • <b>Amount Analysis:</b> {amount_note}<br/>
        • <b>Documentation:</b> {police_note}<br/>
        • <b>Witness Verification:</b> {witness_note}<br/><br/>
        
        <b>Recommended Actions:</b><br/>
        1. Proceed with standard claim processing procedures<br/>
        2. Verify basic information matches records<br/>
        3. Process payment according to policy terms<br/>
        4. Maintain standard documentation requirements<br/><br/>
        
        <b>Note:</b> While this claim appears legitimate, standard verification procedures should 
        still be followed to ensure accuracy and compliance.
        """
    
    story.append(Paragraph(insights_text, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # ========== TECHNICAL DETAILS ==========
    story.append(Paragraph("TECHNICAL ANALYSIS DETAILS", heading_style))
    
    tech_data = [
        ['Parameter', 'Value'],
        ['Prediction Score', f"{fraud_score:.4f}%"],
        ['Model Confidence', f"{(1 - abs(fraud_score/100 - (1 if claim['prediction_label'] == 'Fraud' else 0))) * 100:.2f}%"],
        ['Classification', claim['prediction_label']],
        ['Analysis Date', datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")],
        ['Report Version', '1.0'],
        ['AI Model', 'ClaimWatch AI Fraud Detection v2.0'],
    ]
    
    tech_table = Table(tech_data, colWidths=[2.5*inch, 4.5*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1d4ed8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f6fb')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1f2937')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dbe3f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f9fe')]),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 0.5*inch))
    
    # ========== FOOTER ==========
    footer_text = f"""
    <i>This report was generated by ClaimWatch AI Fraud Detection System.<br/>
    Report ID: CW-{claim['id']:06d} | Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br/>
    For questions or support, contact: insuranceclaimwatchai@gmail.com</i>
    """
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceBefore=20
    )
    story.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph,PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from copy import copy, deepcopy
import DateTime as dt


def make_flowables():
    

    flowables = []
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'Times-Roman'
    styleH = styles['Heading1']
    styleN.textColor = '#043475'
    styleN.fontSize = 14
    p2 = Paragraph('Juteau Johnson Comba Inc', styleN)
    flowables.append(p2)
    # textobject.setFillGray(0.5)
    styleN.textColor = '#808080'
    styleN.fontSize = 10
    styleN.spaceBefore = 5
    # textobject.textLine('Real Estate Appraisers & Consultants')
    p3 = Paragraph('Real Estate Appraisers & Consultants', styleN)
    flowables.append(p3)
    # p.drawText(textobject)

    # textobject = p.beginText()
    # textobject.setTextOrigin(5.887*inch, 2.783*inch)
    # textobject.setFillGray(0)
    # textobject.textLine('Appraisal Report on:')
    # p.drawText(textobject)

    # textobject = p.beginText()
    # textobject.setTextOrigin(6.403*inch, 4.061*inch)
    # textobject.setFillGray(0)
    # textobject.textLine('Appraisal Report on:')
    # p.drawText(textobject)
    # styles = getSampleStyleSheet()
    style_right_big = ParagraphStyle('style_right_big',
    fontSize=16,
    alignment=TA_RIGHT,
    leading=18.5,
    fontName='Times-Roman',
    )
    
    # styles.add(ParagraphStyle(name='RightAlign', alignment=TA_RIGHT))
    # styles.add(ParagraphStyle(name='FontSize', fontSize=16))
    # style_right_align = styles['RightAlign']
    style_right_big2 = deepcopy(style_right_big)
    style_right_big2.textColor = '#043475'
    style_right_big2.spaceBefore = 87.5
    style_right_big2.spaceAfter = 0
    # style_right_big2.leading = 0
    p11 = Paragraph('Appraisal Report on:', style_right_big2)
    flowables.append(p11)
    # style_right_big.textColor = '#000000'
    
    # p1.wrapOn(p, 400, 60)
    # p1.drawOn(p, width-450, 150)
   

    style_right_big3 = deepcopy(style_right_big2)
    style_right_big3.spaceBefore = 38




    style_contactus = deepcopy(styleN)
    style_contactus.alignment = TA_CENTER
    style_contactus.fontSize = 12
    style_contactus.leading = 12
    style_contactus.textColor = '#043475'
    style_contactus.rightIndent = -280
    style_contactus.spaceBefore = 150

    p_contactus = Paragraph('''2255 St. Laurent Blvd.<br/>\
    Suite 340<br/>\
    Ottawa, Ontario<br/>\
    K1G 4K3<br/><br/>\
    www.juteaujohnsoncomba.com<br/><br/>\
    Phone: 613-738-2426<br/>\
    Fax: 613-738-0429<br/><br/>''', style_contactus)
    style_contactus2 = deepcopy(style_contactus)
    style_contactus2.fontSize = 10
    style_contactus2.spaceBefore = 0
    p_contactus2 = Paragraph('<i>© 2022 Juteau Johnson Comba Inc</i>', style_contactus2)
    flowables.append(p_contactus)
    flowables.append(p_contactus2)


    # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()
    flowables.append(PageBreak())

    return flowables

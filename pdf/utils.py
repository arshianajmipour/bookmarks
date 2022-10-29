import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, PageBreak
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from copy import copy, deepcopy
from django.http import FileResponse

class Reporter:
    

    styles = getSampleStyleSheet()


    def __init__(self, report):
        self.flowables = []
        self.report = report

        self.styleN = Reporter.styles['Normal']
        self.styleN.fontName = 'Times-Roman'
        self.styleN.fontSize = 11.5
        self.styleN.leading = 14
        self.styleN.alignment = TA_JUSTIFY
        self.styleN.justifyBreaks = 1

        self.styleH2 = Reporter.styles['Heading2']
        self.styleH2.fontName = 'Times-Roman'

        self.style_header1 = deepcopy(self.styleN)
        self.style_header1.textColor = '#043475'
        self.style_header1.fontSize = 14

        self.style_header2 = deepcopy(self.style_header1)
        self.style_header2.textColor = '#808080'
        self.style_header2.fontSize = 10
        self.style_header2.spaceBefore = 5

        self.style_right_big = ParagraphStyle('style_right_big',
        fontSize=16,
        alignment=TA_RIGHT,
        leading=18.5,
        fontName='Times-Roman',
        )

        self.style_right_big_spaceBefore_big = deepcopy(self.style_right_big)
        self.style_right_big_spaceBefore_big.textColor = '#043475'
        self.style_right_big_spaceBefore_big.spaceBefore = 87.5
        self.style_right_big_spaceBefore_big.spaceAfter = 0

        self.style_right_big_spaceBefore_small = deepcopy(self.style_right_big_spaceBefore_big)
        self.style_right_big_spaceBefore_small.spaceBefore = 38


        self.style_contactus = deepcopy(self.styleN)
        self.style_contactus.alignment = TA_CENTER
        self.style_contactus.fontSize = 12
        self.style_contactus.leading = 12
        self.style_contactus.textColor = '#043475'
        self.style_contactus.rightIndent = -280
        self.style_contactus.spaceBefore = 150

        self.style_contactus2 = deepcopy(self.style_contactus)
        self.style_contactus2.fontSize = 10
        self.style_contactus2.spaceBefore = 0

        self.style_right_small = deepcopy(self.style_right_big)
        self.style_right_small.fontSize = 12

        self.style_left_small = deepcopy(self.style_right_small)
        self.style_left_small.alignment = TA_LEFT

        self.style_left_titr = deepcopy(self.style_right_big)
        self.style_left_titr.alignment = TA_LEFT
        self.style_left_titr.fontSize = 12
        self.style_left_titr.spaceBefore = 10

        self.style_left_context = deepcopy(self.style_left_titr)
        self.style_left_context.fontSize = 11.5
        self.style_left_context.leading = 14
        self.style_left_context.alignment = TA_JUSTIFY
        self.style_left_context.justifyBreaks = 1

        self.style_left_context_spaceAfter = deepcopy(self.style_left_context)
        self.style_left_context_spaceAfter.spaceAfter = 15

        self.style_left_listitem = deepcopy(self.style_left_context)
        self.style_left_listitem.spaceBefore = 0
        self.style_left_listitem.alignment = TA_LEFT

        self.style_contactus_small_center = deepcopy(self.style_contactus)
        self.style_contactus_small_center.fontSize = 10
        self.style_contactus_small_center.spaceBefore = 0
        self.style_contactus_small_center.rightIndent = 0
        self.style_contactus_small_center.spaceBefore = 0

        

    def createTemplate(self):
        self.buffer = io.BytesIO()
        self.template = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            topMargin=inch,
            leftMargin=0.9*inch,
            rightMargin=0.64*inch,
            bottomMargin=0.4*inch
        )

        for i in range(1, 3):
            self.createPage(i)
            self.flowables.append(PageBreak())
        
        return self.buildDoc()

    def buildDoc(self):
        self.template.build(
            self.flowables
        )
        self.buffer.seek(0)
        return FileResponse(self.buffer, as_attachment=True, filename='hello.pdf')


    def createPage(self, page_number):
        FA = self.flowables.append
        page_number = int(page_number)

        if page_number == 1:
            FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )

            FA( Paragraph('Real Estate Appraisers & Consultants', self.style_header2) )

            FA( Paragraph('Appraisal Report on:', self.style_right_big_spaceBefore_big) )
            FA( Paragraph(self.report.location, self.style_right_big) )

            FA( Paragraph('Effective Date:', self.style_right_big_spaceBefore_small) )
            FA( Paragraph(self.report.effective_date.strftime('%b %d, %Y'), self.style_right_big) )

            FA( Paragraph('Report Date:', self.style_right_big_spaceBefore_small) )
            FA( Paragraph(self.report.report_date.strftime('%b %d, %Y'), self.style_right_big) )

            FA( Paragraph('Prepared For:', self.style_right_big_spaceBefore_small) )
            FA( Paragraph(self.report.client_name, self.style_right_big) )


            FA( Paragraph('''2255 St. Laurent Blvd.<br/>\
            Suite 340<br/>\
            Ottawa, Ontario<br/>\
            K1G 4K3<br/><br/>\
            www.juteaujohnsoncomba.com<br/><br/>\
            Phone: 613-738-2426<br/>\
            Fax: 613-738-0429<br/><br/>''', self.style_contactus) )

            FA( Paragraph('<i>© 2022 Juteau Johnson Comba Inc</i>', self.style_contactus2) )
        

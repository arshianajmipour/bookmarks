import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.colors import yellow, green, red, black, gray
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, PageBreak
from reportlab.platypus import ListFlowable, ListItem, Table, TableStyle, Frame, NextPageTemplate, PageTemplate
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from copy import copy, deepcopy
from django.http import FileResponse

class Reporter:
    

    styles = getSampleStyleSheet()


    def __init__(self, report):
        self.flowables = []
        self.report = report
        self.buffer = io.BytesIO()
        self.template = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            topMargin=inch,
            leftMargin=0.9*inch,
            rightMargin=0.64*inch,
            bottomMargin=0.4*inch
        )


        ################################## Paragraph Styles #################################################
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

        self.style_left_context_indent12 = deepcopy(self.style_left_context)
        self.style_left_context_indent12.leftIndent = 12

        self.style_left_listitem = deepcopy(self.style_left_context)
        self.style_left_listitem.spaceBefore = 0
        self.style_left_listitem.alignment = TA_LEFT

        self.style_contactus_small_center = deepcopy(self.style_contactus)
        self.style_contactus_small_center.fontSize = 10
        self.style_contactus_small_center.spaceBefore = 0
        self.style_contactus_small_center.rightIndent = 0
        self.style_contactus_small_center.spaceBefore = 0

        self.style_title = deepcopy(self.styleH2)
        self.style_title.fontSize = 15
        self.style_title.alignment = TA_CENTER

        # self.style_left_titr_big = deepcopy(self.style_left_titr)
        # self.style_left_titr_big.fontSize = 12



        ################################## Table Styles ###################################################
        self.table_style_padding_small = TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0.5),
            ('TOPPADDING', (0, 0), (-1, -1), 0.5),
        ])



        ################################## Templates ###################################################
        frameT = Frame(
            self.template.leftMargin,
            self.template.bottomMargin,
            self.template.width,
            self.template.height, id='normal'
        )
        def makeHeaderFooterMain(canvas, doc):
            import reportlab.rl_config
            reportlab.rl_config.warnOnMissingFontGlyphs = 0
            

            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            # pdfmetrics.registerFont(TTFont('Times-Roman-Italic', './time-roman-italic.ttf'))

            canvas.saveState()
            textobject = canvas.beginText()
            textobject.setTextOrigin(
                doc.leftMargin + 0.1*inch,
                doc.height + doc.bottomMargin + 0.4*inch,
            )
            textobject.setFont("Times-Roman", 10)
            textobject.setFillGray(0.5)
            textobject.textLines(
                '''11966685 Canada Inc.
                Appraisal Report on 1368 Labrie Avenue, Ottawa, Ontario'''
            )
            canvas.drawText(textobject)


            canvas.drawString(
                doc.leftMargin + doc.width - 0.1*inch,
                doc.height + doc.bottomMargin + 0.3*inch,
                "%d" % canvas.getPageNumber()
            )

            canvas.setStrokeColor(gray)
            p = canvas.beginPath()
            p.moveTo(doc.leftMargin + 0.1*inch, doc.height + doc.bottomMargin + 0.2*inch)
            p.lineTo(doc.leftMargin + doc.width, doc.height + doc.bottomMargin + 0.2*inch)
            p.close()
            canvas.drawPath(p)
            # canvas.drawString(inch, 0.75 * inch, "Page %d" % doc.page)
            # canvas.drawString(
            #     self.template.leftMargin,
            #     self.template.height + self.template.bottomMargin + 0.5*inch,
            #     '''11966685 Canada Inc Appraisal Report on 1368 Labrie Avenue, Ottawa, Ontario '''
            # )
            canvas.restoreState()
        self.template.addPageTemplates([PageTemplate(id='main', frames=frameT, onPage=makeHeaderFooterMain)])
        

    def createTemplate(self):

        # for i in range(1, 3):
        self.createPage()
        
        return self.buildDoc()

    def buildDoc(self):
        self.template.build(
            self.flowables
        )
        self.buffer.seek(0)
        return FileResponse(self.buffer, as_attachment=True, filename='hello.pdf')

    def addTemplateToNextPage(self, template_id):
        self.flowables.append(NextPageTemplate(template_id))


    def createPage(self):
        FA = self.flowables.append
        # page_number = int(page_number)

        # if page_number == 1:
        
        #/////////////////////////////////// page 1 ///////////////////////////////////////////////////////
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
            
        FA(PageBreak())

        #/////////////////////////////////// page 2 /////////////////////////////////////////////////////////
        FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )

        FA( Paragraph('Real Estate Appraisers & Consultants', self.style_header2) )

        FA( Paragraph(self.report.report_date.strftime('%b %d, %Y'), self.style_right_small) )
        FA( Paragraph('Reference No. ' + self.report.ref_code, self.style_right_small) )

        FA( Paragraph(self.report.location, self.style_left_small) )
        FA( Paragraph('<br/>Dear ' + self.report.client_name, self.style_left_small) )

        FA( Paragraph("<b>Re:<font color='white'>TTTTT</font>Appraisal Report on " + self.report.location + "</b><br/>", self.style_left_titr) )

        FA( Paragraph('''In accordance with your request, we have inspected the above-noted property in order to provide you with
        an estimate of the current market value of the fee simple interest in the property based on its highest and
        best use, for mortgage financing purposes. The effective date of appraisal is {date}, the date a
        drive-by inspection of the property was completed. Our value estimate is subject to the following
        assumptions and limiting conditions:'''.format(date = self.report.effective_date.strftime('%b %d, %Y')), self.style_left_context_spaceAfter) )

        t = ListFlowable(
            [
                ListItem(Paragraph('the property is free and clear of any mortgage charges or title encumbrances;', self.style_left_listitem), leftIndent=41),
                ListItem(Paragraph('the subject soils are suitable for development;', self.style_left_listitem), leftIndent=41),
                ListItem(Paragraph('the subject property and neighbouring lands are free of environmental contaminants; and', self.style_left_listitem), leftIndent=41),
                ListItem(Paragraph('''there are no servicing constraints or extraordinary costs related to the servicing or development
                of the site.
                ''', self.style_left_listitem), leftIndent=41),
            ], start="➢", bulletType='bullet', leftIndent=20
        )

        FA( t )

        FA( Paragraph('''2255 St. Laurent Blvd.\
        Suite 340\
        Ottawa, Ontario\
        K1G 4K3<br/>\
        Phone: 613-738-2426\
        Fax: 613-738-0429''', self.style_contactus_small_center) )

        FA(PageBreak())
        #/////////////////////////////////// page 3 /////////////////////////////////////////////////////////
        FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )
        FA( Paragraph(' Real Estate Appraisers & Consultants \n \n', self.style_header2) )
        FA( Paragraph('page 2', self.style_left_small) )
        FA( Paragraph('Reference No. ' + self.report.ref_code, self.style_left_small) )
        FA( Paragraph(self.report.report_date.strftime('%b %d, %Y'), self.style_left_small) )

        FA(PageBreak())


        #/////////////////////////////////// page 4 /////////////////////////////////////////////////////////
        FA( Paragraph("AERIAL PHOTOGRAPH OF SUBJECT PROPERTY", self.style_title) )

        self.addTemplateToNextPage('main')
        FA(PageBreak())
        
        #/////////////////////////////////// page 5 /////////////////////////////////////////////////////////
        #/////////////////////////////////// page 6 /////////////////////////////////////////////////////////
        style_title2 = deepcopy(self.style_title)
        style_title2.borderPadding = (100,100,100)
        FA( Paragraph("SUMMARY OF SALIENT FACTS AND IMPORTANT CONCLUSIONS", style_title2) )

        FA( Paragraph("<b>TERMS OF REFERENCE</b>", self.style_left_titr) )

        data = [[Paragraph('Purpose of Appraisal:', self.style_left_context),
                Paragraph('''To estimate the current market value of the fee simple interest
 in the subject site based on its highest and best use. Our value
 estimate is free and clear of mortgage or other encumbrances,
 unless otherwise indicated, and is subject to any assumptions
 and limiting conditions outlined herein.''', self.style_left_context)],
                [Paragraph('Intended Use & User of Appraisal:', self.style_left_context),
                Paragraph('''To assist the client in estimating the current market value of the
subject parcel for mortgage financing purposes. All other uses
are denied. The intended user ofthe report is 11966685 Canada
Inc. only. All other users and/or parties are denied without
written authorization to use this report from Juteau Johnson
Comba Inc.
''', self.style_left_context)],
                [Paragraph('Effective Date of Appraisal: ', self.style_left_context),
                Paragraph(self.report.effective_date.strftime('%b %d, %Y'), self.style_left_context)],
                [Paragraph('Date of Inspection: ', self.style_left_context),
                Paragraph(self.report.effective_date.strftime('%b %d, %Y'), self.style_left_context)]]

        table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
        FA( table )


        FA(Paragraph('<b>PHYSICAL DATA</b>', self.style_left_titr))

        data = [[Paragraph('Location:', self.style_left_context),
                Paragraph('''The subject property is located on the west side of Labrie
Avenue, to the south of Cyrville Road, in theCyrville Industrial
Area, in the east end of the City of Ottawa.''', self.style_left_context)],
                [Paragraph('Municipal Address:', self.style_left_context),
                Paragraph('''1368 Labrie Avenue, Ottawa, Ontario''', self.style_left_context)],
                [Paragraph('Legal Description:', self.style_left_context),
                Paragraph('''The subject property is identified in the Land Registry Office as
Part of Lot 25, Concession 2, Ottawa Front; designated as Part
1 on Plan 4R-11032; in the former City of Gloucester, now in
the City of Ottawa. PIN 04263-0224.''', self.style_left_context)],
                [Paragraph('Site Area:', self.style_left_context),
                Paragraph('14,962 square feet', self.style_left_context)],
                [Paragraph('Zoning:', self.style_left_context),
                Paragraph('''The property recently received a zoning by-law amendment to
TD1[2755] - Transit Oriented Development Zone. A copy of
the Final Letter of Enactment is attached in the addendum of
this report.''', self.style_left_context)],
                [Paragraph('Current Improvements:', self.style_left_context),
                Paragraph('''The property is currently improved with an older two-storey
residential building that is demised into three rental apartment
units.There is a detached garage convertedintooffice space and
a fully enclosed rear yard.''', self.style_left_context)],
                [Paragraph('Proposed Development:', self.style_left_context),
                Paragraph('''The client is proposing to develop the property with a six-storey,
45-unit apartment building.''', self.style_left_context)],
                [Paragraph('Highest and Best Use:', self.style_left_context),
                Paragraph('''Redevelopment of the property with the proposed residential
apartment use.''', self.style_left_context)]]
        table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
        FA( table )

        FA(Paragraph('<b>VALUATION PARAMETERS</b>', self.style_left_titr))


        # style_left_
        data = [[Paragraph('Total Site Area:', self.style_left_context_indent12),
                Paragraph('''14,962 square feet''', self.style_left_context)],
                [Paragraph('Price Per Sq. Ft.:', self.style_left_context_indent12),
                Paragraph('''$135.00''', self.style_left_context)],
                [Paragraph('<b>Market Value Estimate:</b>', self.style_left_context_indent12),
                Paragraph('''<b>$2,020,000</b>''', self.style_left_context)],
                ]
        table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
        table.setStyle(self.table_style_padding_small)
        FA( table )

        FA( PageBreak() )

        #/////////////////////////////////// page 8 /////////////////////////////////////////////////////////
        FA( Paragraph("SCOPE OF THE APPRAISAL", self.style_title) )
        
        FA( Paragraph('''The Scope of the Appraisal describes the extent of the process of collecting, confirming and reporting
data. With respect to the subject property, this involved the following.
''', self.style_left_context_spaceAfter) )
        FA( Paragraph('''The appraisal commenced with a preliminary investigation undertaken to determine market trends,
influences and other significant factors pertinent to the subject property. A drive-by inspection of the
property was completed on {date}, together with the surrounding neighbourhood. The legal
description and site areawere obtained from Geo Warehouse (an on-line service providing access to land
registry data and updated regularly from the POLARIS data base - the automated land records
management system for the Province of Ontario) and are assumed to be correct. Zoning was extracted
from the City of Ottawa’s ZoningBy-law No. 2008-250, as amended and the Final Letter of Enactment
provided by the client, and attached in the addendum to this report. Market data sources included
information contained in our files, the land registry office, and other appraisers, realtors or persons
knowledgeable of the subject property marketplace.'''.format(date=self.report.effective_date.strftime('%b %d, %Y')), self.style_left_context_spaceAfter) )
        FA( Paragraph('''This appraisal complies with our understanding ofthe requirements of the Canadian Uniform Standards
of Professional Appraisal Practice of the Appraisal Institute of Canada. We did not complete technical
investigations such as:''', self.style_left_context_spaceAfter ) )

        t = ListFlowable(
            [
                ListItem(Paragraph('an environmental review of the property;', self.style_left_listitem), leftIndent=1*inch),
                ListItem(Paragraph('a survey of the site;', self.style_left_listitem), leftIndent=1*inch),
                ListItem(Paragraph('investigations into the bearing qualities of the soils.', self.style_left_listitem), leftIndent=1*inch),
            ], start="square", bulletType='bullet', leftIndent=0.8*inch
        )

        FA( t )
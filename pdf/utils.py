import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.colors import yellow, green, red, black, gray
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, PageBreak
from reportlab.platypus.flowables import Flowable, DocAssert
from reportlab.platypus import ListFlowable, ListItem, Table, TableStyle, Frame, NextPageTemplate, PageTemplate
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from copy import copy, deepcopy
from django.http import FileResponse
import logging
import sys

logger = logging.getLogger(__name__)

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, reporter, **kw):
        super().__init__(filename, **kw)
        self._reporter = reporter
    def afterPage(self):
        # logger.error(self.pageTemplate.id)
        currPageTemplate = self.pageTemplate.id
        # if currPageTemplate != None:
        # logger.error(self._reporter.flowables[-1].action[1])
        self._reporter.setTemplateToNextPage(self.pageTemplate.id)
        # self._reporter.setTemplateToNextPage("salam")
        if self.page in (1,2,3):
            # logger.error(self._reporter.flowables[-1].action[1])
            logger.error(currPageTemplate)
        # logger.error(self._reporter.flowables[0])
        # logger.error(currPageTemplate)
        # for i in self._reporter.flowables:
        #     logger.error(i)
        

class Reporter:
    

    styles = getSampleStyleSheet()


    def __init__(self, report):
        self.flowables = []
        self.report = report
        self.buffer = io.BytesIO()
        self.template = MyDocTemplate(
            self.buffer,
            pagesize=letter,
            topMargin=inch,
            leftMargin=0.9*inch,
            rightMargin=0.64*inch,
            bottomMargin=0.75*inch,
            reporter=self
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
        self.style_contactus.spaceBefore = 130

        self.style_contactus2 = deepcopy(self.style_contactus)
        self.style_contactus2.fontSize = 10
        self.style_contactus2.spaceBefore = 0
        self.style_contactus2.spaceAfter = 0

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

        self.style_left_context_indent20 = deepcopy(self.style_left_context)
        self.style_left_context_indent20.leftIndent = 20
 
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
                doc.leftMargin + 0.11*doc.leftMargin,
                doc.height + doc.bottomMargin + 0.405*inch,
            )
            textobject.setFont("Times-Roman", 10)
            textobject.setFillGray(0.5)
            textobject.textLines(
                '''11966685 Canada Inc.
                Appraisal Report on 1368 Labrie Avenue, Ottawa, Ontario'''
            )
            canvas.drawText(textobject)


            canvas.drawString(
                doc.leftMargin + doc.width - 0.12*inch,
                doc.height + doc.bottomMargin + 0.3*inch,
                "%d" % canvas.getPageNumber()
            )

            canvas.setStrokeColor(gray)
            p = canvas.beginPath()
            p.moveTo(doc.leftMargin + 0.11*doc.leftMargin, doc.height + doc.bottomMargin + 0.2*inch)
            p.lineTo(doc.leftMargin + doc.width - 0.07*inch, doc.height + doc.bottomMargin + 0.2*inch)
            p.close()
            canvas.drawPath(p)
            
            canvas.setStrokeColor(gray)
            p = canvas.beginPath()
            p.moveTo(doc.leftMargin + 0.1*inch, 0.9*doc.bottomMargin)
            p.lineTo(doc.leftMargin + doc.width - 0.07*inch, 0.9*doc.bottomMargin)
            p.close()
            canvas.drawPath(p)
            
            textobject = canvas.beginText()
            textobject.setTextOrigin(
                doc.leftMargin + 0.1*inch,
                0.7*doc.bottomMargin,
            )
            textobject.setFont("Times-Roman", 10)
            textobject.setFillGray(0.5)
            textobject.textLine('Juteau Johnson Comba Inc.')
            canvas.drawText(textobject)
            
            def stringWidth2(string, font, size):
                spaces_count = 0
                for char in string:
                    if char.isspace():
                        spaces_count += 1
                width = canvas.stringWidth(string, font, size)
                width += spaces_count
                return width
            textobject = canvas.beginText()
            string = '104-22-31'
            # string = '.'
            font = 'Times-Roman'
            font_size = 10
            
            textobject.setTextOrigin(
                doc.leftMargin + doc.width - canvas.stringWidth(string, font, font_size) - 0.06*inch,
                # doc.leftMargin + doc.width + doc.rightMargin,
                
                0.7*doc.bottomMargin,
            )
            textobject.setFont(font, font_size)
            textobject.setFillGray(0.5)
            textobject.textLine(string)
            canvas.drawText(textobject)
            
            canvas.restoreState()
            
        self.template.addPageTemplates([
            PageTemplate(id='intro', frames=frameT),
            PageTemplate(id='main', frames=frameT, onPageEnd=makeHeaderFooterMain)
        ])
        # logger.error(self.template.pageTemplates[0].autoNextPageTemplate)
        # print >>sys.stderr, "self.template.pageTemplates"

    def insertIntoFlowables(self, index, flowable):
        self.flowables.insert(index, flowable)

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

    def setTemplateToNextPage(self, template_id):
        self.flowables.append(NextPageTemplate(template_id))


    def createPage(self):
        FA = self.flowables.append
        # page_number = int(page_number)

        # if page_number == 1:
        # self.setTemplateToNextPage('intro')
        # FA(DocAssert('doc.pageTemplate.id=="intro"','expected doc.pageTemplate.id=="main"'))
        
        
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
        # FA(DocAssert('doc.pageTemplate.id=="intro"','expected doc.pageTemplate.id=="main"'))
        
        # FA(DocAssert('doc.pageTemplate.id=="introtrbtg"','expected doc.pageTemplate.id=="main"'))
        # logger.error(self.template.docEval('doc.pageTemplate'))
        
        FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )
        FA( Paragraph(' Real Estate Appraisers & Consultants \n \n', self.style_header2) )
        FA( Paragraph('page 2', self.style_left_small) )
        FA( Paragraph('Reference No. ' + self.report.ref_code, self.style_left_small) )
        FA( Paragraph(self.report.report_date.strftime('%b %d, %Y') + '<br/><br/>', self.style_left_small) )
        
        FA( Paragraph('''We have prepared this report for you and your associates. It is not to be reproduced, in whole or in part,
without the written consent of the undersigned. Neither our name nor the material submitted may be
included in any prospectus, newspaper publicity or as part of any printed material, or used in offerings or
representations in connection with the sale of securities or participation interests to the public, without our
prior written consent. The report is only valid if it bears the original signature of the author.''', self.style_left_context_spaceAfter) )
        FA( Paragraph('''Our report providing details of the property and our method of valuation is attached. If we can be of further
assistance in these or other matters, please do not hesitate to contact us.''', self.style_left_context_spaceAfter) )
        FA( Paragraph('''Yours truly,''', self.style_left_context_spaceAfter) )
        
        FA( Paragraph('<b>JUTEAU JOHNSON COMBA INC</b>', self.style_left_context) )
        FA( Paragraph('picture', self.style_left_context) )
        FA( Paragraph('Tania J. McDonald, B.A., AACI, P.App.', self.style_left_context) )
        FA(PageBreak())


        #/////////////////////////////////// page 4 /////////////////////////////////////////////////////////
        FA( Paragraph("AERIAL PHOTOGRAPH OF SUBJECT PROPERTY", self.style_title) )

        FA(PageBreak())
        
        #/////////////////////////////////// page 5 /////////////////////////////////////////////////////////
        self.setTemplateToNextPage('main')
        FA(PageBreak())
        #/////////////////////////////////// page 6 & 7 /////////////////////////////////////////////////////////
        
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
        FA( Paragraph('''Appraisers are not qualified in professional matters like land surveying, engineering, architecture and
the law, nor are they qualified as building inspectors. Investigations into matters such as these do not
form part of an appraiser's investigations. We have assumed that there are no hidden or unapparent
conditions of the property, sub-soil orstructuresthat render it more or less valuable. No responsibility
is assumed forsuch conditions or for arranging for engineering studiesthat may be required to discover
them. Where matters were noted that appeared unusual, they have been noted in this report. The
services of experts in these fields are required to investigate the possibility that defects are present.
''', self.style_left_context_spaceAfter ) )

        FA( Paragraph('''An environmental audit has not been conducted in conjunction with the preparation of thisreport. It is
assumed that hazardoussubstances do not exist. Itshould be clearlyunderstood that we are not qualified
to detect, test for, investigate, or otherwise ascertain the existence of such substances. As such, we do
not assume any responsibility for their existence or any costs associated with their removal, correction,
or treatment, in the event that they are found to exist on the subject property, or on adjacent lands.
Further, it is assumed that soils are suitable to support development.
''', self.style_left_context_spaceAfter ) )

        FA(PageBreak())
    #///////////////////////////////////////// page9 //////////////////////////////////////////////////////
        FA(Paragraph('TERMS OF REFERENCE',self.style_title))
        FA(Paragraph('<B>Purpose of Appraisal</B>',self.style_left_titr))
        FA(Paragraph('''The purpose of this appraisal is to estimate the current market value of the fee simple interest in the
subject property based on its highest and best use. Our value estimate is free and clear of mortgage or
other encumbrances, unless otherwise indicated, and are subject to the following assumptions:'''
            ,self.style_left_context_spaceAfter))
        t = ListFlowable(
            [
                ListItem(Paragraph('the property is free and clear of any mortgage charges or title encumbrances;', self.style_left_listitem), leftIndent=1*inch),
                ListItem(Paragraph('''the subject soils are suitable for development;'''
                    , self.style_left_listitem), leftIndent=1*inch),
                ListItem(Paragraph('the subject property and neighbouring lands are free of environmental contaminants; and', self.style_left_listitem), leftIndent=1*inch),
                ListItem(Paragraph(''' there are no servicing constraints or extraordinary costs related to the servicing or
                    development of the site.''', 
                    self.style_left_listitem), leftIndent=1*inch),
            ]
            , start="square", bulletType='bullet', leftIndent=0.8*inch
        )
        FA(t)
        FA(Paragraph('<B>Intended Use/User of Appraisal</B>',self.style_left_titr))
        FA(Paragraph('''The intended use of the appraisal is to assist the client in estimating the market value of the subject
            property for mortgage financing purposes. The intended user of this appraisal is'''+
            self.report.location+
            '''Liability is expressly denied for any other use or user without our (Juteau Johnson Comba Inc) prior
            written consent.
            ''' , self.style_left_context_spaceAfter))
        FA(Paragraph('<B>Definition of Market Value</B>',self.style_left_titr))
        FA(Paragraph('For the purpose of this appraisal, market value is defined as:',self.style_left_context_spaceAfter))
        FA(Paragraph('''<I>The most probable price, as of a specified date, in cash, or in terms equivalent to cash, or in
            other precisely revealed terms, for which the specified property rights should sell after
            reasonable exposure in a competitive market under all conditions requisite to a fair sale, with
            the buyer and the seller each acting prudently, knowledgeable, and for self-interest, assuming
            that neither is under duress.</I>
            ''',self.style_left_context_indent20))
        FA(Paragraph('<B>Definition of Exposure Time</B>',self.style_left_titr))
        FA(Paragraph('''<I>Exposure time, as per the Canadian Uniform Standards of Professional Appraisal Practice (CUSPAP)
            dated January 1, 2022, may be defined as follows:</I>''',self.style_left_context_indent20))
        FA(Paragraph('''Exposure time is differentfor varioustypes ofreal estate and under variousmarket conditions. Itshould
            be noted that the overall concept of reasonable exposure encompasses not only adequate,sufficient and
            reasonable time but also adequate, sufficient and reasonable effort.''',self.style_left_context_spaceAfter)
        )
        FA(Paragraph('Our valuation is based on a reasonable exposure time of two to four months.',self.style_left_context_spaceAfter))
        FA(Paragraph('<B>Property Rights Under Appraisal</B>',self.style_left_titr))
        FA(Paragraph('''The property ownership right under appraisal is that of the fee simple interest in the subject property.
            Fee simple interest is defined as:''',self.style_left_context_spaceAfter))
        FA(Paragraph('''<I>“...absolute ownership of property unencumbered by any other interest or estate and subject
            only to the powers of government.”
            </I>''',self.style_left_context_indent20))
        FA(Paragraph('<B>Effective Date of Appraisal</B>',self.style_left_titr))
        FA(Paragraph('The effective date of appraisal is'+self.report.effective_date.strftime('%b %d, %Y')
        ,self.style_left_context_spaceAfter))
        FA(Paragraph('<B>Date of Inspection</B>',self.style_left_titr))
        FA(Paragraph('''Inspection, as per theCanadian UniformStandards of Professional Appraisal Practice (CUSPAP) dated'''+
        self.report.report_date.strftime('%b %d, %Y')+'may be defined as follows:',self.style_left_context_spaceAfter))
        FA(Paragraph('''<I>“An observation, site visit, walk through, viewing or non-invasive visual examination
            of a property.”</I>
            ''',self.style_left_context_indent20))
        FA(Paragraph('A drive-by inspection of the subject property was undertaken on'+
        self.report.effective_date.strftime('%b %d, %Y'),self.style_left_context_spaceAfter))
        FA(PageBreak())

        
        
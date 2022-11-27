import io
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.colors import yellow, green, red, black, gray, white
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, PageBreak
from reportlab.platypus.flowables import Flowable, DocAssert, _bulletNames
from reportlab.platypus import ListFlowable, ListItem, Table, TableStyle, Frame, NextPageTemplate, PageTemplate
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from copy import copy, deepcopy
from django.http import FileResponse
import logging
import sys


_bulletNames['diamondsuit'] = '♦'
_bulletNames['right-arrowhead'] = '⮚'

logger = logging.getLogger(__name__)

class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, reporter, **kw):
        super().__init__(filename, **kw)
        self._reporter = reporter
    def beforePage(self):
        # logger.error(self.pageTemplate.id)
        currPageTemplate = self.pageTemplate.id
        # if currPageTemplate != None:
        # logger.error(self._reporter.flowables[-1].action[1])

        # self._reporter.appendNextTemplate(currPageTemplate)
        self._reporter.insertNextTemplateIntoTop(currPageTemplate)

        # self._reporter.appendNextTemplate("salam")
        # if self.page in (1,2,3):
            # logger.error(self._reporter.flowables[-1].action[1])
            # logger.error(currPageTemplate)
        if self.page == 4:
            # logger.error('\tpage')
            # [logger.error(fl.action[1] + '\t' + str(idx)) for idx, fl in enumerate(self._reporter.flowables) if isinstance(fl, NextPageTemplate)]
            # logger.error('\n\n')
            logger.error(self._reporter.flowables[0])
            # logger.error(self._reporter.flowables[130])
            # logger.error(self._reporter.flowables[131])

            # logger.error(self._reporter.flowables[142])

        # logger.error(_bulletNames)
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
            topMargin=1.05*inch,
            leftMargin=0.9*inch,
            rightMargin=0.9*inch,
            bottomMargin=0.75*inch,
            reporter=self
        )


        ################################## Paragraph Styles #################################################
        self.styleN = Reporter.styles['Normal']
        self.styleN.fontName = 'Times-Roman'
        self.styleN.fontSize = 11.7
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
        self.style_right_big_spaceBefore_big.spaceBefore = 92
        self.style_right_big_spaceBefore_big.spaceAfter = 0

        self.style_right_big_spaceBefore_small = deepcopy(self.style_right_big_spaceBefore_big)
        self.style_right_big_spaceBefore_small.spaceBefore = 38


        self.style_contactus = deepcopy(self.styleN)
        self.style_contactus.alignment = TA_CENTER
        self.style_contactus.fontSize = 12
        self.style_contactus.leading = 13
        self.style_contactus.textColor = '#043475'
        self.style_contactus.rightIndent = -310
        self.style_contactus.spaceBefore = 120

        self.style_contactus2 = deepcopy(self.style_contactus)
        self.style_contactus2.fontSize = 8
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
        self.style_left_context.leading = 14
        self.style_left_context.alignment = TA_JUSTIFY
        self.style_left_context.justifyBreaks = 1
        self.style_left_context.spaceBefore = 10

        self.style_left_context_spaceAfter = deepcopy(self.style_left_context)
        self.style_left_context_spaceAfter.spaceAfter = 15

        self.style_left_context_indent12 = deepcopy(self.style_left_context)
        self.style_left_context_indent12.leftIndent = 12

        self.style_left_context_indent20 = deepcopy(self.style_left_context)
        self.style_left_context_indent20.leftIndent = 20

        self.style_left_listitem = deepcopy(self.style_left_context)
        self.style_left_listitem.spaceBefore = 0
        self.style_left_listitem.alignment = TA_LEFT

        self.style_center_context_spaceAfter = deepcopy(self.style_left_context_spaceAfter)
        self.style_center_context_spaceAfter.alignment = TA_CENTER

        self.style_contactus_small_center = deepcopy(self.style_contactus)
        self.style_contactus_small_center.fontSize = 10
        self.style_contactus_small_center.spaceBefore = 0
        self.style_contactus_small_center.rightIndent = 0
        self.style_contactus_small_center.spaceBefore = 0

        self.style_title = deepcopy(self.styleH2)
        self.style_title.fontSize = 14.5
        self.style_title.alignment = TA_CENTER
        self.style_title.spaceAfter = 13

        # self.style_left_titr_big = deepcopy(self.style_left_titr)
        # self.style_left_titr_big.fontSize = 12



        ################################## Table Styles ###################################################
        self.style_table_default = [
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]

        self.style_table_padding_small = deepcopy(self.style_table_default)
        self.style_table_padding_small.extend([
            ('BOTTOMPADDING', (0, 0), (1, 2), 0.5),
            ('TOPPADDING', (0, 0), (1, 2), 0.5),
        ])



        ################################## Templates ###################################################
        frameT = Frame(
            self.template.leftMargin,
            self.template.bottomMargin + 0.15*inch,
            self.template.width,
            self.template.height, id='normal'
        )
        frame_intro1 = Frame(
            self.template.leftMargin,
            self.template.bottomMargin - 0.28*inch,
            self.template.width + 0.225*inch,
            self.template.height * 0.86, id='frame-intro1'
        )
        frame_intro2 = Frame(
            self.template.leftMargin,
            self.template.bottomMargin + 0.15*inch,
            self.template.width + 0.225*inch,
            self.template.height * 0.89, id='frame-intro2'
        )
        def makeHeaderFooterMain(canvas, doc):

            canvas.saveState()
            textobject = canvas.beginText()
            textobject.setTextOrigin(
                doc.leftMargin + 0.11*doc.leftMargin,
                doc.height + doc.bottomMargin + 0.41*inch,
            )
            textobject.setFont("Times-Italic", 10)
            textobject.setFillGray(0.5)
            textobject.textLines(
                '''11966685 Canada Inc.
                Appraisal Report on {0}'''.format(self.report.municipal_address)
            )
            canvas.drawText(textobject)


            canvas.drawRightString(
                doc.leftMargin + doc.width - 0.02*inch,
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
            textobject.setFont("Times-Italic", 10)
            textobject.setFillGray(0.5)
            textobject.textLine('Juteau Johnson Comba Inc.')
            canvas.drawText(textobject)

            string = '104-22-31'
            font = 'Times-Italic'
            font_size = 10

            canvas.setFillGray(0.5)
            canvas.setFont(font, font_size)
            canvas.drawRightString(
                doc.leftMargin + doc.width - 0.06*inch,
                0.7*doc.bottomMargin,
                string
            )

            canvas.restoreState()

        def makeTemplateIntro(canvas, doc):
            canvas.saveState()

            #logo = ImageReader('http://juteaujohnsoncomba.com/wp-content/uploads/2021/09/cropped-cropped-JJC-Logo-vertical-e1631126319540.jpg')
            #logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
            logo = ImageReader(os.path.dirname(os.path.realpath(__file__)) + '/../JJC.png')
            canvas.drawImage(
                logo,
                doc.width + 0.225*inch + doc.leftMargin - 0.6*inch,
                doc.height + doc.bottomMargin - 4.7*inch,
                # 0,
                # 0,
                preserveAspectRatio=True,
                width=0.46*inch,
                # height=2*inch
            )

            textobject = canvas.beginText()
            textobject.setTextOrigin(
                doc.leftMargin + 0.16*inch,
                doc.bottomMargin + doc.height - 0.1*inch,
            )
            textobject.setFont("Times-Roman", 14)
            textobject.setFillColor('#043475')
            textobject.textLine('Juteau Johnson Comba Inc')
            textobject.setTextOrigin(
                doc.leftMargin + 0.16*inch,
                doc.bottomMargin + doc.height - 0.27*inch,
            )
            textobject.setFont("Times-Roman", 10)
            textobject.setFillColor(black)
            textobject.setFillGray(0.5)
            textobject.textLine('Real Estate Appraisers & Consultants')

            canvas.drawText(textobject)

            canvas.setStrokeColor('#043475')
            canvas.line(
                x1=doc.leftMargin + 0.03*inch,
                y1=doc.bottomMargin + doc.height + 0.65*inch,
                x2=doc.leftMargin + 0.03*inch,
                y2=doc.bottomMargin + doc.height + 0.16*inch
            )

            canvas.line(
                x1=doc.leftMargin + 0.03*inch,
                y1=doc.bottomMargin + doc.height - 0.3*inch,
                x2=doc.leftMargin + 0.03*inch,
                y2=doc.bottomMargin
            )

            canvas.line(
                x1=doc.leftMargin * 0.48,
                y1=doc.bottomMargin + doc.height - 0.397*inch,
                x2=doc.leftMargin + doc.width * 0.57,
                y2=doc.bottomMargin + doc.height - 0.397*inch
            )



            # FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )

            # FA( Paragraph('Real Estate Appraisers & Consultants', self.style_header2) )

            canvas.restoreState()

        def makeTemplateIntro2(canvas, doc):
            canvas.saveState()

            #logo = ImageReader('http://juteaujohnsoncomba.com/wp-content/uploads/2021/09/cropped-cropped-JJC-Logo-vertical-e1631126319540.jpg')
            #logo = ImageReader('https://www.google.com/images/srpr/logo11w.png')
            logo = ImageReader(os.path.dirname(os.path.realpath(__file__)) + '/../JJC.png')
            canvas.drawImage(
                logo,
                doc.width + 0.225*inch + doc.leftMargin - 0.6*inch,
                doc.height + doc.bottomMargin - 4.7*inch,
                # 0,
                # 0,
                preserveAspectRatio=True,
                width=0.46*inch,
                # height=2*inch
            )

            textobject = canvas.beginText()
            textobject.setTextOrigin(
                doc.leftMargin + 0.45*inch,
                doc.bottomMargin + doc.height - 0.1*inch,
            )
            textobject.setFont("Times-Roman", 14)
            textobject.setFillColor('#043475')
            textobject.textLine('Juteau Johnson Comba Inc')
            textobject.setTextOrigin(
                doc.leftMargin + 0.45*inch,
                doc.bottomMargin + doc.height - 0.27*inch,
            )
            textobject.setFont("Times-Roman", 10)
            textobject.setFillColor(black)
            textobject.setFillGray(0.5)
            textobject.textLine('Real Estate Appraisers & Consultants')

            canvas.drawText(textobject)

            canvas.setStrokeColor('#043475')
            canvas.line(
                x1=doc.leftMargin + 0.03*inch,
                y1=doc.bottomMargin + doc.height + 0.65*inch,
                x2=doc.leftMargin + 0.03*inch,
                y2=doc.bottomMargin + doc.height + 0.16*inch
            )

            canvas.line(
                x1=doc.leftMargin + 0.03*inch,
                y1=doc.bottomMargin + doc.height - 0.3*inch,
                x2=doc.leftMargin + 0.03*inch,
                y2=doc.bottomMargin
            )

            canvas.line(
                x1=doc.leftMargin * 0.48,
                y1=doc.bottomMargin + doc.height - 0.397*inch,
                x2=doc.leftMargin + doc.width * 0.57,
                y2=doc.bottomMargin + doc.height - 0.397*inch
            )

            canvas.setFillColor('#043475')
            canvas.drawCentredString(
                doc.leftMargin + doc.width * 0.58,
                doc.bottomMargin,
                '2255 St. Laurent Blvd. Suite 340 Ottawa, Ontario K1G 4K3'
            )
            canvas.drawCentredString(
                doc.leftMargin + doc.width * 0.58,
                doc.bottomMargin - 0.2*inch,
                'Phone: 613-738-2426 Fax: 613-738-0429'
            )

            canvas.restoreState()

        self.template.addPageTemplates([
            PageTemplate(id='intro', frames=frame_intro1, onPageEnd=makeTemplateIntro),
            PageTemplate(id='intro2', frames=frame_intro2, onPageEnd=makeTemplateIntro2),
            PageTemplate(id='blank', frames=frameT),
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

    def appendNextTemplate(self, template_id):
        self.flowables.append(NextPageTemplate(template_id))

    def insertNextTemplateIntoTop(self, template_id):
        self.flowables.insert(0, NextPageTemplate(template_id))


    def insertParagraphWithTitle(self, title, context, style_title=None, style_context=None):
        if style_title == None:
            style_title = self.style_left_context_spaceAfter
        if style_context == None:
            style_context = self.style_left_context_spaceAfter

        FA = self.flowables.append

        FA( Paragraph('<b>' + title + '</b>', style_title) )
        FA( Paragraph(context, style_context) )

    def insertParagraph(self, context, style_context=None, font_size=None):
        if style_context == None:
            style_context = self.style_left_context_spaceAfter
        if font_size != None:
            style_context.fontSize = font_size
        FA = self.flowables.append
        FA( Paragraph(context, style_context) )

    def insertKeyContextTable(self, *tuples, style_key=None, style_context=None, style_table=None):
        FA = self.flowables.append
        if style_key == None:
            style_key = self.style_left_context
        if style_context == None:
            style_context = self.style_left_context
        if style_table == None:
            style_table = self.style_table_default
        data = []
        # logger.error(len(args))
        # for i in range(0, len(args), 2):
        for tuplee in tuples:
            if tuplee[0] == 'Frontage':
                style_context = deepcopy(style_context)
                style_context.alignment = TA_LEFT
            # elif style_context == self.style_left_context:
            else:
                style_context = self.style_left_context
            data.append([Paragraph(tuplee[0] + ':', style_key), Paragraph(tuplee[1], style_context)])

        table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
        # if style_table == None:
        table.setStyle(TableStyle(style_table))
        FA( table )


    def insertQoute(self, context, left_indent=None):
        style = deepcopy(self.style_left_context_indent20)
        if left_indent != None:
            style.leftIndent = left_indent

        FA = self.flowables.append
        FA(Paragraph('<I>' + context + '</I>', style))


    def insertList(self, items, left_indent_item,
                left_indent_bullet, _bullet, _start=None, style_item=None,):

        FA = self.flowables.append
        if style_item == None:
            style_item = self.style_left_listitem

        list_items = []
        for item in items:
            list_items.append(ListItem(Paragraph(item, style_item), leftIndent=left_indent_item))

        t = ListFlowable(
            list_items, start=_start, bulletType=_bullet, leftIndent=left_indent_bullet
        )

        FA( t )

    def createPage(self):
        FA = self.flowables.append
        # page_number = int(page_number)

        # if page_number == 1:
        # self.appendNextTemplate('intro')
        # FA(DocAssert('doc.pageTemplate.id=="intro"','expected doc.pageTemplate.id=="main"'))


        #/////////////////////////////////// page 1 ///////////////////////////////////////////////////////
        # FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )

        # FA( Paragraph('Real Estate Appraisers & Consultants', self.style_header2) )

        FA( Paragraph('Appraisal Report on:', self.style_right_big_spaceBefore_big) )
        FA( Paragraph(self.report.subject_property, self.style_right_big) )

        FA( Paragraph('Effective Date:', self.style_right_big_spaceBefore_small) )
        # FA( Paragraph(self.report.effective_date.strftime('%b %d, %Y'), self.style_right_big) )
        FA( Paragraph(self.report.getEffectiveDateAsString(), self.style_right_big) )


        FA( Paragraph('Report Date:', self.style_right_big_spaceBefore_small) )
        # FA( Paragraph(self.report.report_date.strftime('%b %d, %Y'), self.style_right_big) )
        FA( Paragraph(self.report.getReportCompleteDateAsString(), self.style_right_big) )

        FA( Paragraph('Prepared For:', self.style_right_big_spaceBefore_small) )
        FA( Paragraph(self.report.client_legal_name, self.style_right_big) )

        FA( Paragraph('''2255 St. Laurent Blvd.<br/>\
        Suite 340<br/>\
        Ottawa, Ontario<br/>\
        K1G 4K3<br/><br/>\
        www.juteaujohnsoncomba.com<br/><br/>\
        Phone: 613-738-2426<br/>\
        Fax: 613-738-0429<br/><br/>''', self.style_contactus) )

        FA( Paragraph('<i>© 2022 Juteau Johnson Comba Inc</i>', self.style_contactus2) )

        self.appendNextTemplate('intro2')
        FA(PageBreak())

        #/////////////////////////////////// page 2 /////////////////////////////////////////////////////////
        # FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )

        # FA( Paragraph('Real Estate Appraisers & Consultants', self.style_header2) )

        FA( Paragraph(self.report.getReportCompleteDateAsString(), self.style_right_small) )
        FA( Paragraph('Reference No. ' + self.report.file_no, self.style_right_small) )

        FA( Paragraph(self.report.client_legal_name, self.style_left_small) )
        FA( Paragraph(self.report.client_address, self.style_left_small) )
        FA( Paragraph('<br/>Dear ' + self.report.client_name, self.style_left_small) )

        FA( Paragraph("<b>Re:<font color='white'>TTTTT</font>Appraisal Report on " + self.report.subject_property + "</b><br/>", self.style_left_titr) )

        FA( Paragraph('''In accordance with your request, we have inspected the above-noted property in order to provide you with
        an estimate of the current market value of the fee simple interest in the property based on its highest and
        best use, for {purposes} purposes. The effective date of appraisal is {date}, the date a
        {appraisal_type} of the property was completed. Our value estimate is subject to the following
        assumptions and limiting conditions:'''.format(date = self.report.getEffectiveDateAsString(), purposes=self.report.purpose, appraisal_type=self.report.appraisal_type), self.style_left_context_spaceAfter) )

        # t = ListFlowable(
        #     [
        #         ListItem(Paragraph('the property is free and clear of any mortgage charges or title encumbrances;', self.style_left_listitem), leftIndent=41),
        #         ListItem(Paragraph('the subject soils are suitable for development;', self.style_left_listitem), leftIndent=41),
        #         ListItem(Paragraph('the subject property and neighbouring lands are free of environmental contaminants; and', self.style_left_listitem), leftIndent=41),
        #         ListItem(Paragraph('''there are no servicing constraints or extraordinary costs related to the servicing or development
        #         of the site.
        #         ''', self.style_left_listitem), leftIndent=41),
        #     ], start="➢", bulletType='bullet', leftIndent=20
        # )

        # FA( t )

        self.insertList(items=[
            'the property is free and clear of any mortgage charges or title encumbrances;',
            'the subject soils are suitable for development;',
            'the subject property and neighbouring lands are free of environmental contaminants; and',
            '''there are no servicing constraints or extraordinary costs related to the servicing or development of the site.'''
            ],
            _start="➢", _bullet='bullet', left_indent_item=41, left_indent_bullet=20
        )

        self.insertParagraph('''Based on our investigations and analysis of the relevant data, as well as the foregoing terms of reference
and assumptions, it is our opinion that the market value of the fee simple interest in {loc},
based on its highest and best use, as at {date}, is:'''.format(date=self.report.getEffectiveDateAsString(), loc=self.report.subject_property))

        FA( Paragraph('''<b>TWO MILLION AND TWENTY THOUSAND DOLLARS<br/>\
($2,020,000)</b>''', self.style_center_context_spaceAfter) )

        self.insertParagraph('<br/><br/><br/>.../2', self.style_right_small)


        # FA( Paragraph('''2255 St. Laurent Blvd.\
        # Suite 340\
        # Ottawa, Ontario\
        # K1G 4K3<br/>\
        # Phone: 613-738-2426\
        # Fax: 613-738-0429''', self.style_contactus_small_center) )

        FA(PageBreak())
        #/////////////////////////////////// page 3 /////////////////////////////////////////////////////////
        # FA(DocAssert('doc.pageTemplate.id=="intro"','expected doc.pageTemplate.id=="main"'))

        # FA(DocAssert('doc.pageTemplate.id=="introtrbtg"','expected doc.pageTemplate.id=="main"'))
        # logger.error(self.template.docEval('doc.pageTemplate'))

        # FA( Paragraph('Juteau Johnson Comba Inc', self.style_header1) )
        # FA( Paragraph(' Real Estate Appraisers & Consultants \n \n', self.style_header2) )
        FA( Paragraph('page 2', self.style_left_small) )
        FA( Paragraph('Reference No. ' + self.report.ref_code, self.style_left_small) )
        FA( Paragraph(self.report.getReportCompleteDateAsString() + '<br/><br/>', self.style_left_small) )

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

        self.appendNextTemplate('blank')
        FA(PageBreak())


        #/////////////////////////////////// page 4 /////////////////////////////////////////////////////////
        FA( Paragraph("AERIAL PHOTOGRAPH OF SUBJECT PROPERTY", self.style_title) )

        FA(PageBreak())

        #/////////////////////////////////// page 5 /////////////////////////////////////////////////////////
        self.appendNextTemplate('main')
        FA(PageBreak())
        #/////////////////////////////////// page 6 & 7 /////////////////////////////////////////////////////////

        style_title2 = deepcopy(self.style_title)
        style_title2.borderPadding = (100,100,100)
        FA( Paragraph("SUMMARY OF SALIENT FACTS AND IMPORTANT CONCLUSIONS", style_title2) )

        FA( Paragraph("<b>TERMS OF REFERENCE</b>", self.style_left_titr) )

#         data = [[Paragraph('Purpose of Appraisal:', self.style_left_context),
#                 Paragraph('''To estimate the current market value of the fee simple interest
#  in the subject site based on its highest and best use. Our value
#  estimate is free and clear of mortgage or other encumbrances,
#  unless otherwise indicated, and is subject to any assumptions
#  and limiting conditions outlined herein.''', self.style_left_context)],
#                 [Paragraph('Intended Use & User of Appraisal:', self.style_left_context),
#                 Paragraph('''To assist the client in estimating the current market value of the
# subject parcel for mortgage financing purposes. All other uses
# are denied. The intended user ofthe report is 11966685 Canada
# Inc. only. All other users and/or parties are denied without
# written authorization to use this report from Juteau Johnson
# Comba Inc.
# ''', self.style_left_context)],
#                 [Paragraph('Effective Date of Appraisal: ', self.style_left_context),
#                 Paragraph(self.report.effective_date.strftime('%b %d, %Y'), self.style_left_context)],
#                 [Paragraph('Date of Inspection: ', self.style_left_context),
#                 Paragraph(self.report.effective_date.strftime('%b %d, %Y'), self.style_left_context)]]

#         table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
#         FA( table )

        self.insertKeyContextTable(
            ('Purpose of Appraisal', '''To estimate the current market value of the fee simple interest
 in the subject site based on its highest and best use. Our value
 estimate is free and clear of mortgage or other encumbrances,
 unless otherwise indicated, and is subject to any assumptions
 and limiting conditions outlined herein.'''),
            ('Intended Use & User of Appraisal', '''To assist the client in estimating the current market value of the
subject parcel for mortgage financing purposes. All other uses
are denied. The intended user ofthe report is 11966685 Canada
Inc. only. All other users and/or parties are denied without
written authorization to use this report from Juteau Johnson
Comba Inc.'''),
            ('Effective Date of Appraisal', self.report.effective_date.strftime('%b %d, %Y')),
            ('Date of Inspection', self.report.effective_date.strftime('%b %d, %Y'))
        )


        FA(Paragraph('<b>PHYSICAL DATA</b>', self.style_left_titr))

#         data = [[Paragraph('Location:', self.style_left_context),
#                 Paragraph('''The subject property is located on the west side of Labrie
#                     Avenue, to the south of Cyrville Road, in theCyrville Industrial
#                     Area, in the east end of the City of Ottawa.''', self.style_left_context)],
#                 [Paragraph('Municipal Address:', self.style_left_context),
#                 Paragraph('''{0}''', self.style_left_context)],
#                 [Paragraph('Legal Description:', self.style_left_context),
#                 Paragraph('''The subject property is identified in the Land Registry Office as
#                     Part of Lot 25, Concession 2, Ottawa Front; designated as Part
#                     1 on Plan 4R-11032; in the former City of Gloucester, now in
#                     the City of Ottawa. PIN 04263-0224.''', self.style_left_context)],
#                 [Paragraph('Site Area:', self.style_left_context),
#                 Paragraph('{site_area} square feet', self.style_left_context)],
#                 [Paragraph('Zoning:', self.style_left_context),
#                 Paragraph('''The property recently received a zoning by-law amendment to
# TD1[2755] - Transit Oriented Development Zone. A copy of
# the Final Letter of Enactment is attached in the addendum of
# this report.''', self.style_left_context)],
#                 [Paragraph('Current Improvements:', self.style_left_context),
#                 Paragraph('''The property is currently improved with an older two-storey
# residential building that is demised into three rental apartment
# units.There is a detached garage convertedintooffice space and
# a fully enclosed rear yard.''', self.style_left_context)],
#                 [Paragraph('Proposed Development:', self.style_left_context),
#                 Paragraph('''The client is proposing to develop the property with a six-storey,
# 45-unit apartment building.''', self.style_left_context)],
#                 [Paragraph('Highest and Best Use:', self.style_left_context),
#                 Paragraph('''Redevelopment of the property with the proposed residential
# apartment use.''', self.style_left_context)]]
#         table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
#         FA( table )

        self.insertKeyContextTable(
            ('Location', '''The subject property is located on the west side of Labrie
                    Avenue, to the south of Cyrville Road, in theCyrville Industrial
                    Area, in the east end of the City of Ottawa.'''),
            ('Municipal Address', '''{0}'''.format(self.report.municipal_address)),
            ('Legal Description', '''The subject property is identified in the Land Registry Office as
                    Part of Lot 25, Concession 2, Ottawa Front; designated as Part
                    1 on Plan 4R-11032; in the former City of Gloucester, now in
                    the City of Ottawa. PIN 04263-0224.'''),
            ('Site Area', '{site_area} square feet'.format(site_area=self.report.site_area)),
            ('Zoning', '''The property recently received a zoning by-law amendment to
TD1[2755] - Transit Oriented Development Zone. A copy of
the Final Letter of Enactment is attached in the addendum of
this report.'''),
            ('Current Improvements', '''The property is currently improved with an older two-storey
residential building that is demised into three rental apartment
units.There is a detached garage convertedintooffice space and
a fully enclosed rear yard.'''),
            ('Proposed Development', '''The client is proposing to develop the property with a six-storey,
45-unit apartment building.'''),
            ('Highest and Best Use', '''Redevelopment of the property with the proposed residential
apartment use.'''),
        )

        FA(Paragraph('<b>VALUATION PARAMETERS</b>', self.style_left_titr))


        # data = [[Paragraph('Total Site Area:', self.style_left_context_indent12),
        #         Paragraph('''{site_area} square feet''', self.style_left_context)],
        #         [Paragraph('Price Per Sq. Ft.:', self.style_left_context_indent12),
        #         Paragraph('''$135.00''', self.style_left_context)],
        #         [Paragraph('<b>Market Value Estimate:</b>', self.style_left_context_indent12),
        #         Paragraph('''<b>$2,020,000</b>''', self.style_left_context)],
        #         ]
        # table = Table(data, colWidths=[self.template.width * 2 / 5, self.template.width * 3 / 5])
        # table.setStyle(self.style_table_padding_small)
        # FA( table )

        self.insertKeyContextTable(
            ('Total Site Area', '''{site_area} square feet'''.format(site_area=self.report.site_area)),
            ('Price Per Sq. Ft.', '''$135.00'''),
            ('<b>Market Value Estimate:</b>', '''<b>$2,020,000</b>'''),
            style_key=self.style_left_context_indent12,
            style_context=self.style_left_context,
            style_table=self.style_table_padding_small
        )

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

        # t = ListFlowable(
        #     [
        #         ListItem(Paragraph('an environmental review of the property;', self.style_left_listitem), leftIndent=1*inch),
        #         ListItem(Paragraph('a survey of the site;', self.style_left_listitem), leftIndent=1*inch),
        #         ListItem(Paragraph('investigations into the bearing qualities of the soils.', self.style_left_listitem), leftIndent=1*inch),
        #     ], start="square", bulletType='bullet', leftIndent=0.8*inch
        # )

        # FA( t )

        self.insertList(items=[
            'an environmental review of the property;',
            'a survey of the site;',
            'investigations into the bearing qualities of the soils.',
        ], _bullet='bullet', left_indent_item=1*inch, left_indent_bullet=0.8*inch)

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
    #///////////////////////////////////////// page 9 & 10 //////////////////////////////////////////////////////
        FA(Paragraph('TERMS OF REFERENCE',self.style_title))
        FA(Paragraph('<B>Purpose of Appraisal</B>',self.style_left_titr))
        FA(Paragraph('''The purpose of this appraisal is to estimate the current market value of the fee simple interest in the
subject property based on its highest and best use. Our value estimate is free and clear of mortgage or
other encumbrances, unless otherwise indicated, and are subject to the following assumptions:'''
            ,self.style_left_context_spaceAfter))
        # t = ListFlowable(
        #     [
        #         ListItem(Paragraph('the property is free and clear of any mortgage charges or title encumbrances;', self.style_left_listitem), leftIndent=1*inch),
        #         ListItem(Paragraph('''the subject soils are suitable for development;'''
        #             , self.style_left_listitem), leftIndent=1*inch),
        #         ListItem(Paragraph('the subject property and neighbouring lands are free of environmental contaminants; and', self.style_left_listitem), leftIndent=1*inch),
        #         ListItem(Paragraph(''' there are no servicing constraints or extraordinary costs related to the servicing or
        #             development of the site.''',
        #             self.style_left_listitem), leftIndent=1*inch),
        #     ]
        #     , start="square", bulletType='bullet', leftIndent=0.8*inch
        # )
        # FA(t)

        self.insertList(
            items=[
                'the property is free and clear of any mortgage charges or title encumbrances;',
                '''the subject soils are suitable for development;''',
                'the subject property and neighbouring lands are free of environmental contaminants; and',
                ''' there are no servicing constraints or extraordinary costs related to the servicing or
                    development of the site.''',
            ],
            _bullet='bullet', left_indent_item=1*inch, left_indent_bullet=0.8*inch
        )

        FA(Paragraph('<B>Intended Use/User of Appraisal</B>',self.style_left_titr))
        FA(Paragraph('''The intended use of the appraisal is to assist the client in estimating the market value of the subject
            property for mortgage financing purposes. The intended user of this appraisal is'''+
            self.report.location+
            '''Liability is expressly denied for any other use or user without our (Juteau Johnson Comba Inc) prior
            written consent.
            ''' , self.style_left_context_spaceAfter))
        FA(Paragraph('<B>Definition of Market Value</B>',self.style_left_titr))
        FA(Paragraph('For the purpose of this appraisal, market value is defined as:',self.style_left_context_spaceAfter))
        # FA(Paragraph('''<I>The most probable price, as of a specified date, in cash, or in terms equivalent to cash, or in
        #     other precisely revealed terms, for which the specified property rights should sell after
        #     reasonable exposure in a competitive market under all conditions requisite to a fair sale, with
        #     the buyer and the seller each acting prudently, knowledgeable, and for self-interest, assuming
        #     that neither is under duress.</I>
        #     ''',self.style_left_context_indent20))
        self.insertQoute('''The most probable price, as of a specified date, in cash, or in terms equivalent to cash, or in
            other precisely revealed terms, for which the specified property rights should sell after
            reasonable exposure in a competitive market under all conditions requisite to a fair sale, with
            the buyer and the seller each acting prudently, knowledgeable, and for self-interest, assuming
            that neither is under duress.
            ''')
        self.insertParagraph('''The foregoing definitionwas extracted fromtheCanadian UniformStandards of Professional Appraisal
Practice (CUSPAP) dated January 1, 2022.''')
        FA(Paragraph('<B>Definition of Exposure Time</B>',self.style_left_titr))
        # FA(Paragraph('''<I>Exposure time, as per the Canadian Uniform Standards of Professional Appraisal Practice (CUSPAP)
        #     dated January 1, 2022, may be defined as follows:</I>''',self.style_left_context_indent20))
        self.insertQoute('''Exposure time, as per the Canadian Uniform Standards of Professional Appraisal Practice (CUSPAP)
            dated January 1, 2022, may be defined as follows:''')
        FA(Paragraph('''Exposure time is differentfor varioustypes ofreal estate and under variousmarket conditions. Itshould
            be noted that the overall concept of reasonable exposure encompasses not only adequate,sufficient and
            reasonable time but also adequate, sufficient and reasonable effort.''',self.style_left_context_spaceAfter)
        )
        FA(Paragraph('Our valuation is based on a reasonable exposure time of two to four months.',self.style_left_context_spaceAfter))
        FA(Paragraph('<B>Property Rights Under Appraisal</B>',self.style_left_titr))
        FA(Paragraph('''The property ownership right under appraisal is that of the fee simple interest in the subject property.
            Fee simple interest is defined as:''',self.style_left_context_spaceAfter))
        # FA(Paragraph('''<I>“...absolute ownership of property unencumbered by any other interest or estate and subject
        #     only to the powers of government.”
        #     </I>''',self.style_left_context_indent20))
        self.insertQoute('''“...absolute ownership of property unencumbered by any other interest or estate and subject
            only to the powers of government.”''')
        FA(Paragraph('<B>Effective Date of Appraisal</B>',self.style_left_titr))
        FA(Paragraph('The effective date of appraisal is'+self.report.effective_date.strftime('%b %d, %Y')
            ,self.style_left_context_spaceAfter))
        FA(Paragraph('<B>Date of Inspection</B>',self.style_left_titr))
        FA(Paragraph('''Inspection, as per theCanadian UniformStandards of Professional Appraisal Practice (CUSPAP) dated'''+
            self.report.getReportCompleteDateAsString()+'may be defined as follows:',self.style_left_context_spaceAfter))
        # FA(Paragraph('''<I>“An observation, site visit, walk through, viewing or non-invasive visual examination
        #     of a property.”</I>
        #     ''',self.style_left_context_indent20))
        self.insertQoute('''“An observation, site visit, walk through, viewing or non-invasive visual examination
            of a property.”''')
        FA(Paragraph('A drive-by inspection of the subject property was undertaken on'+
            self.report.effective_date.strftime('%b %d, %Y'),self.style_left_context_spaceAfter))
        FA(PageBreak())


    #///////////////////////////////////////// page 11 //////////////////////////////////////////////////////
        FA( Paragraph('PROPERTY IDENTIFICATION', self.style_title) )

        self.insertParagraphWithTitle('Location', '''The subject site is located on the west side of Labrie Avenue, to the south of Cyrville Road, in the Cyrville Industrial Park, in the east end of the City of Ottawa.''')

        self.insertParagraphWithTitle('Municipal Address', '''The subject's municipal address is {0}.'''.format(self.report.municipal_address))

        self.insertParagraphWithTitle('Legal Description', '''The subject property is legally described as Part of Lot 25, Concession 2, Ottawa Front; designated as
Part 1 on Plan 4R-11032; in the former City of Gloucester, now in the City of Ottawa. It is identified
in the Land Registry Office under PIN 04263-0224.''')

        FA( Paragraph('''The foregoing legal description wastaken from GeoWarehouse (an on-line service providing accessto
land registry data and updated regularly from the POLARIS data base - the automated land records
management system for the Province of Ontario). It is assumed to be correct, however, should not be
relied uponas accuratewithout obtaininga qualified legal opinion. We havemade noinvestigationsinto
the title of the property. Further, any documentsregistered on title have not been read. Thisreport has
been prepared on the premise that the property is free and clear of all liens and encumbrances, unless
otherwise indicated, and on the assumption that the improvements do not encroach on any adjoining
lands.''', self.style_left_context_spaceAfter) )

        self.insertParagraphWithTitle('Ownership and Three Year Sales History', '''Based on a search ofthe Geowarehouse web site, the subject propertywaslast transferred on September
4, 2020 to 11966685 Canada Inc. from Jamal and IbrahimBaroud for a consideration of $760,000. We
are not aware of any listings, offers or agreements of purchase and sale affecting the property over the
past three years''')

        self.insertParagraphWithTitle('Assessment and Taxes', '''Based upon theCity of Ottawa tax bill provided by the client, realty taxes were $3,495.65 in 2021 based
on an assessment of $536,000. Ontario’s planned reassessment for the 2021-2024 assessment cycle
based on 2019 values has been delayed for a second year due to the Covid-19 Pandemic. Assessments
for 2022 will continue to be based on the current 2016 value''')

        self.appendNextTemplate('blank')
        FA( PageBreak() )

    #///////////////////////////////////////// page 12 //////////////////////////////////////////////////////
        FA( Paragraph('LOCATION MAP', self.style_title) )

        FA( PageBreak() )
    #///////////////////////////////////////// page 13, 14, 15 //////////////////////////////////////////////////////
    #///////////////////////////////////////// page 16, 17, 18, 19, 20, 21, 22 //////////////////////////////////////////////////////
    #///////////////////////////////////////// page 23 //////////////////////////////////////////////////////
        FA( Paragraph('SITE DATA<br/>', self.style_title) )

        self.insertKeyContextTable(
            ('Location', '''West side of Labrie Avenue, to the south of Cyrville Road, in
the Cyrville Industrial Area in the east nd of the City of Ottawa.'''),
            ('Configuration', 'The subject site has a rectangular configuration.'),
            ('Frontage', '''- 100.64 feet of frontage along the west side of Labrie Avenue;<br/>\
- 148.85 feet along the southern boundary;<br/>\
- 101.02 feet along the western boundary; and<br/>\
- 148.43 feet along the northern boundary'''),
            ('Site Area', '{site_area} square feet'.format(site_area=self.report.site_area)),
            ('Topography', 'The overall site has a slight upward slope from the road grade.'),
            ('Access', '''Vehicular access is available via two points of ingress/egress
from the west side of Labrie Avenue.'''),
            ('Site Services', '''Full municipal services are available to the subject site
including water, hydro, telephone, gas and sanitary sewers.'''),
            ('Site Improvements', '''The front yard is sodded. An older asphalt driveway and
parking area are located in the southeastern portion of the site.
A compact gravel driveway is located along the northern
elevation of the building. The rear yard comprises a fully
fenced compact gravel storage area that is leased.'''),
            ('Soil Conditions', '''No soil tests were completed in conjunction with thisreport. It
is assumed that soils are suitable to support the existing
improvements.'''),
            ('Environmental Concerns', '''Our report assumes that the property is free of environmental
contaminates or hazardous substances (including mould).
However, it should be clearly understood that we are not
qualified to detect, test for, investigate, or otherwise ascertain
the existence of such substances. As such, we do not assume
any responsibility for their existence or any costs associated
with their removal, correction, or treatment in the event that
they are found to exist on the subject property or on adjacent
lands.'''),
        )


        self.appendNextTemplate('blank')
        FA( PageBreak() )

    #///////////////////////////////////////// page 24 //////////////////////////////////////////////////////
        FA( Paragraph('ZONING MAP', self.style_title) )

        FA( PageBreak() )

    #///////////////////////////////////////// page 25 & 26 //////////////////////////////////////////////////////
        FA( Paragraph('LAND USE REGULATIONS', self.style_title) )
        self.insertParagraph('''The subject property recently received a zoning by-law amendment from a Light Industrial Zone to a
TD1[2755] - h - Transit Oriented Development Zone. A copy of the Final Letter of Enactment is
attached in the addendumofthisreport. In accordance with theCityof Ottawa’s comprehensive zoning
by-law (2008-250) that was approved by City Council on June 25, 2008, the purpose of the Transit
Oriented Development is to:''')

#         self.insertQoute('''(1) Establish minimum density targets needed to support Light Rail Transit (LRT) use for
# lands within Council approved Transit Oriented Development Plan areas;<br/><br/>\
# (2) Accommodate a wide range of transit-supportive land uses such as residential, office,
# commercial, retail, arts and culture, entertainment, service and institutional uses in a
# compact pedestrian-oriented built form at medium to high densities;<br/><br/>\
# (3) Locate higher densitiesin proximity toLRTstationsto create focal points of activity and
# promote the use of multiple modes of transportation; and,<br/><br/>\
# (4) Impose development standards that ensure the development of attractive urban
# environments that exhibit high-quality urban design and that establish priority streets
# for active use frontages and streetscaping investment.''', 40)

        self.insertList(
            items=[
                '''<I>Establish minimum density targets needed to support Light Rail Transit (LRT) use for
lands within Council approved Transit Oriented Development Plan areas;</I>''',
                '''<I>Accommodate a wide range of transit-supportive land uses such as residential, office,
commercial, retail, arts and culture, entertainment, service and institutional uses in a
compact pedestrian-oriented built form at medium to high densities;</I>''',
                '''<I>Locate higher densitiesin proximity toLRTstationsto create focal points of activity and
promote the use of multiple modes of transportation; and,</I>''',
                '''<I>Impose development standards that ensure the development of attractive urban
environments that exhibit high-quality urban design and that establish priority streets
for active use frontages and streetscaping investment.</I>'''
            ],
            _bullet='1', _start='(', left_indent_item=55, left_indent_bullet=15, style_item=self.style_left_context_spaceAfter
        )

        self.insertParagraph('''The TD zone permits a variety of non-residential usesincluding a bank, bar, cinema, community centre,
diplomatic mission, court house, group home, hospital, hotel, instructional facility, library, medical
facility, museum, nightclub, office, place of assembly, post office, post-secondary educational
institution, production studio, recreational or athletic facility, research and development centre,
residential care facility, restaurant, retail store, school, service and repair shop, shelter, sports arena,
technology industry, theatre, training centre, parking garage (subject to being in the same building or on
the same lot as a use or uses listed above), among others.''')
        self.insertParagraph('''Permitted residential uses include an apartment dwelling (low and mid-high rise), planned unit
development, retirement home, rooming house (converted), stacked and townhouse dwelling, among
others.''')
        self.insertParagraph('''The subject property is subject to a holding designation which prohibits any development on the property
until:''')

#         t = ListFlowable(
#             [
#                 ListItem(Paragraph('''A Site PlanApplication is approved, including the registration of an agreement pursuant
# to Section 41 of the Planning Act to the satisfaction of the General Manager, Planning,
# Infrastructure and Economic Development; and''', self.style_left_listitem), leftIndent=70),
#                 ListItem(Paragraph('''Such time as it is demonstrated to the satisfaction of Planning Infrastructure and
# Economic Development that there is availability of and connection to municipal storm
# water infrastructure.''', self.style_left_listitem), leftIndent=70),
#             ], bulletType='i', leftIndent=30
#         )

#         FA( t )

        self.insertList(
            items=[
                '''A Site PlanApplication is approved, including the registration of an agreement pursuant
to Section 41 of the Planning Act to the satisfaction of the General Manager, Planning,
Infrastructure and Economic Development; and''',
                '''Such time as it is demonstrated to the satisfaction of Planning Infrastructure and
Economic Development that there is availability of and connection to municipal storm
water infrastructure.'''
            ],
            _bullet='i', left_indent_item=70, left_indent_bullet=30
        )


        self.insertParagraph('''In the TD1 sub-zone on lots greater than 0.3 acresin size the minimum number of residential units per
hectare is 150 and the minimum floor space index for non-residential use is 0.5 times the site area. In
accordance with Exception 2755 applicable to the subject property, the following are site specific
provisions:''')
        # t = ListFlowable(
        #     [
        #         ListItem(Paragraph('''Minimum interior side yard setback of 3 m on one side, and 6 m on the other; and''', self.style_left_listitem), leftIndent=70),
        #         ListItem(Paragraph('''Minimum rear yard setback 6.5 m''', self.style_left_listitem), leftIndent=70),
        #     ], bulletType='bullet', start='-', leftIndent=30
        # )

        # FA( t )
        self.insertList(
            items=[
                '''Minimum interior side yard setback of 3 m on one side, and 6 m on the other; and''',
                '''Minimum rear yard setback 6.5 m''',
            ],
            _start='-', _bullet='bullet', left_indent_item=70, left_indent_bullet=30
        )

        self.insertParagraph('''In summary, the subject site is zoned for a number of commercial and residential uses, with a holding
designation restricting development until various planning steps are approved. The proposed subject
improvements appear to represent a permitted use under the zoning by-law and to conform to the
applicable zoning regulations. It is our understanding the client is progressing well with their proposal
and the City of Ottawa officials are showing a positive interest in the project. However, a compliance
report from the City of Ottawa would be required to verify that this is the case.''')


        FA( PageBreak() )
    #///////////////////////////////////////// page 27 //////////////////////////////////////////////////////
        FA( Paragraph('HIGHEST AND BEST USE', self.style_title) )

        self.insertParagraph('''Highest and Best Use may be defined as, "that use from among reasonably, probable and legal
alternativeuses,foundtobe physicallypossible, appropriatelysupported,financiallyfeasible, andwhich
results in the highest land value."''')
        self.insertParagraph('''Interpretation of the foregoing includes a realization that the use must be physically possible, legal
and/or probable, there is demand for the use, it is financially feasible hence profitable, and it yieldsthe
highest return to the land.''')
        self.insertParagraph('''The subject is located on the west side of Labrie Avenue, to the south of Cyrville Road, in the Cyrville
Industrial Park in the east end of the City of Ottawa. It islocated within 600metres oftheCyrville LRT
station, as well as proximate to residential developments and other commercial amenities.''')
        self.insertParagraph('''The site is {site_area} square feet in size with approximately 100.64 feet of frontage along the west side of
Labrie Avenue. While the property is currently improved, the client in proposing to redevelop the
property with a six-storey, 45-unit residential apartment building.'''.format(site_area=self.report.site_area))
        self.insertParagraph('''The property just recently received a zoning by-law amendment from a Light Industrial Zone to a
TD1[2755] - h - Transit Oriented Development Zone. There is a holding on the zoning until such time
asthe clientreceivesSite Plan approval and adequate servicing. In accordancewith theTransitOriented
Development zoning, variousresidential and non-residential uses are permitted. The subject’sproposed
development appears to be a permitted use in accordance with the amended zoning by-law.''')
        self.insertParagraph('''Consideration has been given to the residentialrental apartmentmarket which has been performing very
well over the past few years. The subject islocated in the East Ottawa Surrounding Area sub-zone with
vacancy reported at 0.4% as at October 2020 which has decreased from the same time the previous year
when it was at 0.9%. It is also much lower than the overall average for the City at 4.0%. Average
monthly rents reported for the East Ottawa Surrounding Area sub-zone were $1,017 in 2019 and
increased to $1,367 in 2020, a 34.5% increase year over year.''')
        self.insertParagraph('''In conclusion, given the site parcel’s size, recent re-zoning and location, it is our opinion the Highest
and Best Use of the subject, would be its development with a residential apartment use, as proposed.''')

        FA( PageBreak() )
    #///////////////////////////////////////// page 28 & 29 & 30 //////////////////////////////////////////////////////
        FA( Paragraph('VALUATION', self.style_title) )

        self.insertParagraph('''In order to estimate the current market value of the subject property, the Direct Comparison Approach
has been used. In the Direct Comparison Approach to valuation,sales ofsimilarsites are analyzed and
compared to the subject. The sale prices of the comparables are then adjusted for any differences in
comparison to the site under appraisal.''')
        self.insertParagraph('''The following comparable land sales have been analyzed in order to estimate the current market value
of the subject site. Details of the comparable sales analyzed are presented in the appendix and are
summarized as follows:''')



        style = deepcopy(self.style_left_context)
        style.fontSize = 9
        style.alignment = TA_LEFT
        style2 = deepcopy(style)
        style2.textColor = white
        style3 = deepcopy(style2)
        style3.alignment = TA_CENTER
        data = [
            [Paragraph('<b>COMPARABLE LAND SALES</b>', style3), '', '', '', '', '', '',],
            [Paragraph('<b>No.</b>', style3), Paragraph('<b>Location</b>', style3), Paragraph('<b>Date of Sale</b>', style3),
             Paragraph('<b>Zoning</b>', style3), Paragraph('<b>Site Area (Sq. Ft.)</b>', style3),
              Paragraph('<b>Price</b>', style3), Paragraph('<b>Price Per Sq. Ft.</b>', style3)],
            ['1', Paragraph('1200 Lemieux Street & 1209 St. Laurent Boulevard', style), Paragraph('Jul/21 & Nov/20', style), 'TD3', '45,951', '$6,050,000', '$132'],
            ['Subject:', Paragraph('1368 Labrie Avenue', style2), 'Sept/20', '$760,000', '{site_area}'.format(site_area=self.report.site_area),],
        ]

        table_style = deepcopy(self.style_table_default)
        table_style.extend([
                ('SPAN', (0, 0), (6, 0)),
                ('ALIGNMENT', (0,0), (-1,-1), 'CENTER'),
                ('BACKGROUND', (0, 0), (6, 1), black),
                ('BACKGROUND', (0, -1), (-1, -1), black),
                ('TEXTCOLOR', (0,0), (6,1), white),
                ('TEXTCOLOR', (0, -1), (-1, -1), white),
                ('FONTSIZE', (0,0), (-1,-1) , style.fontSize),
                ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
                ('BOX', (0,0), (-1, -1), 1, black),
            ])
        table = Table(data, style=table_style,
            colWidths=[self.template.width * 0.08, self.template.width * 0.2, self.template.width * 0.15, None, None, None, None]
        )

        FA( table )




        self.insertParagraph('''The comparable sales have been analyzed on the basis oftheir price persquare foot and indicate a range
of between $117 and $162 per square foot, with three of the five sales ranging between $132 and $140
per square foot. Adjustments must be made to the indicated sale price per square foot for each sale in
order to reconcile important differences between the comparable sales and the subject property.
Attributessuch as overall location, date ofsale, development potential and physical characteristicswere
taken into consideration.''')
        self.insertParagraph('''<b>Comparable Sale #1, Lemieux Street & St. Laurent Boulevard,</b> is the purchase of two adjacent
parcels that were acquired separately. The assembled property is bound by St. Laurent Boulevard,
Lemieux Street and the extension of Labelle Street, to the south of Ogilvie Road, acrossthe street from
the St. Laurent Shopping Centre, approximately one kilometre to the west of the subject property. The
property was zoned TD3, a superior zoning relative to the subject, and is considered to have a superior
location with good visibility. A downward adjustment to the rate per square foot has been recognized
for the zoning and location. However, an offsetting upward adjustment to the rate per square foot is
warranted for the subject’s smaller site area and for the passage of time since the sale dates. It should
be noted that the property hassubsequently sold at a much higher consideration, but included extensive
development approvals and plans which is not comparable to the current status of the subject property.''')
        self.insertParagraph('''<b>Comparable Sale #2, Tremblay Road,</b> representsthe sale of an assembled property that islocated on
the southwest corner of Tremblay and Belfast Roads as well as the east side of Avenue L, in the East
Industrial neighbourhood, approximately 2.5 kilometres to the west of the subject. The property was
improved with two older office buildings at the time of sale. However, there was a March 2021 Site
Plan proposing the development of the property with a six-storey residential apartment building with
ground floor retailspace. Similar to the subject, the property was zoned TD1 and islocated within 600
metres of a light rail transitstation. While an upward adjustment to the rate persquare foot is necessary
for the passage of time since the date of sale, an offsetting downward adjustment is necessary for the
comparable’s superior location at a busy intersection and it’s shorter development horizon.''')
        self.insertParagraph('''<b>Comparable Sale #3, Montreal Road,</b> is the sale of a slightly smaller sized parcel that is located on
the southeast corner of Montreal Road and Borthwick Avenue, approximately three kilometres to the
north of the subject. The property islocated 300 metresto the west of Montfort Hospital. The property
was improved with two older structures, however, a land study completed by the vendor determined a
six-storey residential building with 30 apartment units and ground floor retail could be constructed on
the site. The subject is considered to have a shorter development horizon and is located in good
proximity to the Cyrville light rail transitstation, for which an upward adjustment to the rate persquare
foot is considered to be necessary. However, a more than offsetting downward adjustment has been
applied for the comparable’s superior location with frontage on two streets, including Montreal Road
which is a busy commercial arterial with public transit. Additionally, the comparable is within walking
distance to the Montfort Hospital which is a major employment centre.''')
        self.insertParagraph('''<b>Comparable Sale #4, Avenue L,</b> is an older sale of a much larger sized property with frontage and
access onto four streets, including the south side of Tremblay Road. The property is located to the
immediate east of the Ottawa Train Station and approximately three kilometres to the west of the
subject. The property isimproved with a large manufacturing facility. The purchasers completed a sale
leaseback for a three-yeartermat marketrent. The purchasersintend to redevelop the site with amixeduse high density development. Given the passage of time and the comparable’s superior zoning and
higher density development potential, a downward adjustment to the rate per square foot is considered
to be warranted. However, a more than offsetting upward adjustment is necessary for the passage of
time since the date of sale and for the subject’s smaller site and shorter development horizon.''')
        self.insertParagraph('''<b>Comparable Sale #5, Smyth Road,</b> is an older sale of a much larger sized site that is located on the
southeast corner of Smyth Road and Othello Avenue, to the immediate north of Elmvale Shopping
Centre, approximately three kilometres to the south of the subject. The property was zoned Arterial
Mainstreet and at the time ofsale there was a June 2019 approved site plan to develop the property with
a nine-storey residential apartment building with ground floor retail space. The purchaser benefitted
from the site plan/approvals in place, for which a downward adjustment to the rate per square foot is
warranted. However, an upward adjustment has been recognized for the passage of time since the date
of sale and for the subject’s much smaller site area.''')

        self.insertParagraph('''The foregoing salesindicate a range of prices between $117 and $162 per square foot, with three of the
five sales ranging between $132 and $140 per square foot.''')
        self.insertParagraph('''Consideration has also been given to the previoussale of the subject in September 2020 at $760,000 or
$50.80 per square foot of site area. The property was improved with a residential triplex and a
freestandingoffice unit. Theownersubsequentlycompletedextensive renovations,increasedrentalrates
and created an enclosed rearstorage yard which has also been leased. This has provided the client with
continued income while they prepare for mid-term redevelopment of the site. The ownersubsequently
submitted a Zoning By-law Amendment application to rezone the site to permit a medium density
residential development. The client recently received rezoning approval as outlined in the Final Letter
ofEnactment attached in the addendumofthisreport and isworkingwith theCityofOttawa to complete
all necessary approvals to redevelop the property with a six-storey, 45-unit residential apartment
building. Given the foregoing, a significant increase to the 2020 purchase price per square foot is
considered to be necessary given the passage of time, the strong demand and limited supply of
redevelopment lands within the urban area of the city and for the progress and approvals obtained from
the City of Ottawa since the date of sale.''')
        self.insertParagraph('''Having regard to the foregoing sales and analysis, it is our opinion that the current market value of the
fee simple interest in the subjectsite based on its highest and best use warrants a value within the range
ofthe comparable sales, namely $135.00 persquare foot ofsite area. Therefore, the market value ofthe
fee simple interest in the subject site, as at January 25, 2022, is estimated as follows:''')

        FA( Paragraph('{site_area} x $135.00 per square foot = $2,019,870'.format(site_area=self.report.site_area), self.style_center_context_spaceAfter) )

        self.insertParagraph('Rounded to:')

        FA( Paragraph('''<b>TWO MILLION AND TWENTY THOUSAND DOLLARS<br/>\
($2,020,000)</b>''', self.style_center_context_spaceAfter) )

        FA( PageBreak() )


    #///////////////////////////////////////// page 31 & 32 & 33 & 34 //////////////////////////////////////////////////////

    #///////////////////////////////////////// page 31 & 32 & 33 & 34 //////////////////////////////////////////////////////
        FA( Paragraph('CERTIFICATION', self.style_title) )
        self.insertParagraphWithTitle('Re:<font color="white">TT</font>Appraisal Report on {0}'.format(self.report.municipal_address),
        '''I certify to the best of my knowledge and belief that:''')


        style = deepcopy(self.style_left_listitem)
        style.alignment = TA_JUSTIFY
        self.insertList(
            items=[
                'The statements of fact contained in this report are true and correct.',
                '''The reported analyses, opinions, and conclusions are limited only by the reported assumptions and
limiting conditions, and are my personal, impartial, and unbiased professional analyses, opinions,
and conclusions.''',
                '''I have no past, present or prospective interest in the property that isthe subject of thisreport and no
personal and/or professional interest or conflict with respect to the parties involved with this
assignment.''',
                '''I have no bias with respect to the property that is the subject matter of this report or to the parties
involved with this assignment.''',
                '''My engagement in and compensation for this assignment were not contingent upon developing or
reporting predetermined results, the amount of the value estimate, or a conclusion favouring the
client or the occurrence of a subsequent event.''',
                '''My analyses, opinions, and conclusions were developed, and this report has been prepared, in
conformity with the Canadian Uniform Standards of Professional Appraisal Practice (CUSPAP).''',
                '''I have the knowledge, skills and experience to complete the assignment competently, and where
applicable this report is co-signed in compliance with CUSPAP.''',
                '''Except as herein disclosed, no one provided professional assistance or third party professional
assistance to the person(s) signing this report.''',
                '''As ofthe date ofthisreport, the undersigned hasfulfilled the requirements ofTheAppraisalInstitute
of Canada's (AIC's) Continuing Professional Development Program.''',
                '''The undersigned is a member in good standing of the Appraisal Institute of Canada.''',
                '''I did personally complete a drive-by inspection of the subject property of the report on January 25, 2022.''',
                '''Based upon the data, analyses and conclusions contained herein, it is our opinion that the market
value ofthe fee simple interest in the subject propertybased on its highest and best use, as atJanuary
24, 2022, is <b>$2,020,000</b>.''',
            ],
            _bullet='bullet', _start='diamondsuit', left_indent_item=20, left_indent_bullet=20,
            style_item=style
        )
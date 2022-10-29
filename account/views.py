from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph
from .models import Profile, Report
from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm, ReportForm
from .utils import make_flowables


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


# @login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def add_report(request):
    if request.method == 'POST':
        report_form = ReportForm(request.POST)
        if report_form.is_valid():
            new_report = report_form.save(commit=False)
            new_report.save()
            return HttpResponseRedirect(reverse('submit_done'))
    else:
        report_form = ReportForm()
    return render(request,
                  'account/report_form.html',
                  {'report_form': report_form, 'section': 'add_report'})


class ReportListView(ListView):
    template_name = 'account/view_reports.html'
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = Report.objects.all()
        context['section'] = 'view_reports'
        return context


@login_required
def submit_done(request):
    return render(request, 'account/submit_done.html', )










































@login_required
def get_pdf2(request,report_id):
    
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.units import inch

    report = Report.objects.get(id=report_id)
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer, bottomup = 0, pagesize = letter)
    my_doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=inch,
            leftMargin=0.9*inch,
            rightMargin=0.64*inch,
            bottomMargin=0.4*inch
    )
    width, height = letter

    # select = int(select)
    # if select == 1:
        # p.drawString(100, 100, report.client_name)
    # if select == 2:
    from reportlab.platypus import Paragraph, PageBreak
    from reportlab.platypus import ListFlowable, ListItem
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
    from copy import copy, deepcopy
    import DateTime as dt


    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'Times-Roman'
    styleH = styles['Heading1']

    flowables = []

    FA = flowables.append


    #/////////////////////////////////// page 1 ///////////////////////////////////
    # textobject = p.beginText()
    # textobject.setTextOrigin((2-0.62)*inch, inch)
    # textobject.setFont("Helvetica-Oblique", 14)
    # textobject.textLine('Juteau Johnson Comba Inc')
    styleN.textColor = '#043475'
    styleN.fontSize = 14
    FA( Paragraph('Juteau Johnson Comba Inc', styleN) )
    # textobject.setFillGray(0.5)
    styleN.textColor = '#808080'
    styleN.fontSize = 10
    styleN.spaceBefore = 5
    # textobject.textLine('Real Estate Appraisers & Consultants')
    FA( Paragraph('Real Estate Appraisers & Consultants', styleN) )
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
    FA( Paragraph('Appraisal Report on:', style_right_big2) )
    # style_right_big.textColor = '#000000'
    FA( Paragraph(report.location, style_right_big) )
    # p1.wrapOn(p, 400, 60)
    # p1.drawOn(p, width-450, 150)

    style_right_big3 = deepcopy(style_right_big2)
    style_right_big3.spaceBefore = 38

    FA( Paragraph('Effective Date:', style_right_big3) )
    FA( Paragraph(report.effective_date.strftime('%b %d, %Y'), style_right_big) )

    FA( Paragraph('Report Date:', style_right_big3) )
    FA( Paragraph(report.report_date.strftime('%b %d, %Y'), style_right_big) )

    FA( Paragraph('Prepared For:', style_right_big3) )
    FA( Paragraph(report.client_name, style_right_big) )


    style_contactus = deepcopy(styleN)
    style_contactus.alignment = TA_CENTER
    style_contactus.fontSize = 12
    style_contactus.leading = 12
    style_contactus.textColor = '#043475'
    style_contactus.rightIndent = -280
    style_contactus.spaceBefore = 150

    FA( Paragraph('''2255 St. Laurent Blvd.<br/>\
    Suite 340<br/>\
    Ottawa, Ontario<br/>\
    K1G 4K3<br/><br/>\
    www.juteaujohnsoncomba.com<br/><br/>\
    Phone: 613-738-2426<br/>\
    Fax: 613-738-0429<br/><br/>''', style_contactus) )

    style_contactus2 = deepcopy(style_contactus)
    style_contactus2.fontSize = 10
    style_contactus2.spaceBefore = 0
    FA( Paragraph('<i>© 2022 Juteau Johnson Comba Inc</i>', style_contactus2) )

    # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()

    #/////////////////////////////////// page 2 ///////////////////////////////////
    FA(PageBreak())
    styleN.textColor = '#043475'
    styleN.fontSize = 14
    FA( Paragraph('Juteau Johnson Comba Inc', styleN) )
    # textobject.setFillGray(0.5)
    styleN.textColor = '#808080'
    styleN.fontSize = 10
    styleN.spaceBefore = 5
    # textobject.textLine('Real Estate Appraisers & Consultants')
    FA( Paragraph('Real Estate Appraisers & Consultants', styleN) )

    style_right_small = ParagraphStyle('style_right_small',
    fontSize=12,
    alignment=TA_RIGHT,
    leading=18.5,
    fontName='Times-Roman',
    )
    FA( Paragraph(report.report_date.strftime('%b %d, %Y'), style_right_small) )
    FA( Paragraph('Reference No. ' + report.ref_code, style_right_small) )

    style_left_small = deepcopy(style_right_small)
    style_left_small.alignment = TA_LEFT
    FA( Paragraph(report.location, style_left_small) )
    FA( Paragraph('<br/>Dear ' + report.client_name, style_left_small) )

    style_left_titr = deepcopy(style_right_big)
    style_left_titr.alignment = TA_LEFT
    style_left_titr.fontSize = 12
    style_left_titr.spaceBefore = 10
    FA( Paragraph("<b>Re:<font color='white'>TTTTT</font>Appraisal Report on " + report.location + "</b><br/>", style_left_titr) )

    
    style_left_context = deepcopy(style_left_titr)
    style_left_context.fontSize = 11.5
    style_left_context.leading = 14
    style_left_context.alignment = TA_JUSTIFY
    style_left_context.justifyBreaks = 1

    style_left_context_spaceAfter = deepcopy(style_left_context)
    style_left_context_spaceAfter.spaceAfter = 15
    FA( Paragraph('''In accordance with your request, we have inspected the above-noted property in order to provide you with
    an estimate of the current market value of the fee simple interest in the property based on its highest and
    best use, for mortgage financing purposes. The effective date of appraisal is {date}, the date a
    drive-by inspection of the property was completed. Our value estimate is subject to the following
    assumptions and limiting conditions:'''.format(date = report.effective_date.strftime('%b %d, %Y')), style_left_context_spaceAfter) )

    style_left_listitem = deepcopy(style_left_context)
    style_left_listitem.spaceBefore = 0
    style_left_listitem.alignment = TA_LEFT
    t = ListFlowable(
        [
            ListItem(Paragraph('the property is free and clear of any mortgage charges or title encumbrances;', style_left_listitem), leftIndent=41),
            ListItem(Paragraph('the subject soils are suitable for development;', style_left_listitem), leftIndent=41),
            ListItem(Paragraph('the subject property and neighbouring lands are free of environmental contaminants; and', style_left_listitem), leftIndent=41),
            ListItem(Paragraph('''there are no servicing constraints or extraordinary costs related to the servicing or development
            of the site.
            ''', style_left_listitem), leftIndent=41),
        ], start="➢", bulletType='bullet', leftIndent=20
    )

    FA( t )

    style_contactus3= deepcopy(style_contactus)
    style_contactus3.fontSize = 10
    style_contactus3.spaceBefore = 0
    style_contactus3.rightIndent =0
    style_contactus3.spaceBefore = 0
    FA( Paragraph('''2255 St. Laurent Blvd.\
    Suite 340\
    Ottawa, Ontario\
    K1G 4K3<br/>\
    Phone: 613-738-2426\
    Fax: 613-738-0429''', style_contactus3) )
    
    #////////////////////////////////page3//////////////////////////////////////

    FA( PageBreak() )
    styleN.textColor = '#043475'
    styleN.fontSize = 14
    FA( Paragraph('Juteau Johnson Comba Inc', styleN) )
    # textobject.setFillGray(0.5)
    styleN.textColor = '#808080'
    styleN.fontSize = 10
    styleN.spaceBefore = 5
    # textobject.textLine('Real Estate Appraisers & Consultants')
    FA( Paragraph(' Real Estate Appraisers & Consultants \n \n', styleN) )
    FA( Paragraph('page 2', style_left_small) )
    FA( Paragraph('\n Reference No. ' + report.ref_code, style_left_small) )
    FA( Paragraph(report.report_date.strftime('%b %d, %Y'), style_left_small) )

    my_doc.build(
        flowables
    )

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')





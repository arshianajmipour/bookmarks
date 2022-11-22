from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Report(models.Model):
    # DROPDOWN_CHOICES = (
    #     (1, 'A'),
    #     (2, 'B'),
    #     (3, 'C'),
    # )
    # RADIO_BUTTON_CHOICES = (
    #     (1, 'select 1'),
    #     (2, 'select 2'),
    #     (3, 'select 3'),
    # )
    subject_property = models.CharField(max_length=255, null=True, blank=False, verbose_name='Subject Property')
    # client_name = models.CharField(max_length=300, null=True, blank=False, verbose_name='Client Name')
    report_completion_date = models.DateField(null=True, blank=False, verbose_name='Report completion date')
    effective_date = models.DateField(null=True, blank=False, verbose_name='Effective Date/Insepction date')


    client_legal_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Client legal name')
    client_address = models.CharField(max_length=255, null=True, blank=False, verbose_name='Client address')
    client_name = models.CharField(max_length=255, null=True, blank=False, verbose_name='Client name')

    purpose = models.CharField(max_length=255, null=True, blank=False, verbose_name='Purpose')
    appraisal_type = models.CharField(max_length=255, null=True, blank=False, verbose_name='Appraisal type')

    file_no = models.CharField(max_length=255, null=True, blank=False, verbose_name='File No.')

    appraiser_sign = models.ImageField(upload_to='uploads/', null=True, blank=False, verbose_name='Appraiser Signature')
    appraiser_name_and_credentials = models.CharField(max_length=255, null=True, blank=False, verbose_name='Appraiser name & credentials')

    abutting_streets = models.TextField(null=True, blank=False, verbose_name='Abutting streets')
    legal_description = models.TextField(null=True, blank=False, verbose_name='Legal description')

    pin_no = models.CharField(max_length=255, null=True, blank=False, verbose_name='Pin No.')
    site_area = models.FloatField(null=True, blank=False, verbose_name='Site Area(Sqr. Ft.)')
    zoning = models.CharField(max_length=255, null=True, blank=False, verbose_name='Zoning')

    current_improvement = models.TextField(null=True, blank=False, verbose_name='Current Improvements')

    proposed_development = models.TextField(null=True, blank=False, verbose_name='Proposed development')
    highest_best_use = models.TextField(null=True, blank=False, verbose_name='Highest best use')
    price_per_sq_ft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='Price per sqr. ft.')
    market_value_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False, verbose_name='Market value estimate')
    # firstname = models.CharField(max_length=300, null=True, blank=False, verbose_name='First Name')
    # lastname = models.CharField(max_length=300, null=True, blank=False, verbose_name='Last Name')
    # email = models.CharField(max_length=300, null=True, blank=False, verbose_name='Email Address')
    # phone_number = models.CharField(max_length=300, null=True, blank=False, verbose_name='Phone Number')
    # location = models.TextField(max_length=300, null=True, blank=False, verbose_name='Location')
    # municipal_address = models.TextField(max_length=300, null=True, blank=False, verbose_name='Municipal Address')
    
    # latitude = models.FloatField(null=True, blank=False, verbose_name='Latitude')
    # longitude = models.FloatField(null=True, blank=False, verbose_name='Longitude')
    # dropdown_feature = models.IntegerField(choices=DROPDOWN_CHOICES, blank=False, null=True,
    #                                        verbose_name='Dropdown Feature')
    # textarea1 = models.TextField(max_length=300, null=True, blank=False, verbose_name='TextArea 1')
    # textarea2 = models.TextField(max_length=300, null=True, blank=False, verbose_name='TextArea 2')
    # textarea3 = models.TextField(max_length=300, null=True, blank=False, verbose_name='TextArea 3')
    # radio_button_feature = models.IntegerField(choices=RADIO_BUTTON_CHOICES, null=True, blank=False,
    #                                            verbose_name='Radio Button Feature')
    # receive_newsletter = models.BooleanField(null=True, blank=False, verbose_name='Receive NewsLetter')
    # fpdf = models.FileField(upload_to='reports/%Y/%m/%d/',null=True, blank=False, verbose_name='Report File')

    def getEffectiveDateAsString(self):
        return self.effective_date.strftime('%b %d, %Y')
    def getReportCompleteDateAsString(self):
        return self.report_completion_date.strftime('%b %d, %Y')
    

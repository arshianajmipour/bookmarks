from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Report(models.Model):
    DROPDOWN_CHOICES = (
        (1, 'A'),
        (2, 'B'),
        (3, 'C'),
    )
    RADIO_BUTTON_CHOICES = (
        (1, 'select 1'),
        (2, 'select 2'),
        (3, 'select 3'),
    )
    client_name = models.CharField(max_length=300, null=True, blank=True, verbose_name='Client Name')
    report_date = models.DateField(null=True, blank=True, verbose_name='Report Date')
    effective_date = models.DateField(null=True, blank=True, verbose_name='Effective Date')
    ref_code = models.CharField(max_length=300, null=True, blank=True, verbose_name='Ref Code')
    firstname = models.CharField(max_length=300, null=True, blank=True, verbose_name='First Name')
    lastname = models.CharField(max_length=300, null=True, blank=True, verbose_name='Last Name')
    email = models.CharField(max_length=300, null=True, blank=True, verbose_name='Email Address')
    phone_number = models.CharField(max_length=300, null=True, blank=True, verbose_name='Phone Number')
    location = models.TextField(max_length=300, null=True, blank=True, verbose_name='Location')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitude')
    dropdown_feature = models.IntegerField(choices=DROPDOWN_CHOICES, blank=True, null=True,
                                           verbose_name='Dropdown Feature')
    textarea1 = models.TextField(max_length=300, null=True, blank=True, verbose_name='TextArea 1')
    textarea2 = models.TextField(max_length=300, null=True, blank=True, verbose_name='TextArea 2')
    textarea3 = models.TextField(max_length=300, null=True, blank=True, verbose_name='TextArea 3')
    radio_button_feature = models.IntegerField(choices=RADIO_BUTTON_CHOICES, null=True, blank=True,
                                               verbose_name='Radio Button Feature')
    receive_newsletter = models.BooleanField(null=True, blank=True, verbose_name='Receive NewsLetter')
    fpdf = models.FileField(upload_to='reports/%Y/%m/%d/',null=True, blank=True, verbose_name='Report File')
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('get_pdf2/<report_id>',views.get_pdf2 , name='get_pdf2'),
    path('get_pdf3/<report_id>',views.get_pdf3 , name='get_pdf3'),
]
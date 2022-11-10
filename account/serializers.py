from rest_framework import serializers
from .models import Report

report_all_fields = [f.name for f in Report._meta.fields]
report_all_fields = tuple(report_all_fields)

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        # fields = ('client_name', 'report_date', 'effective_date')
        fields = report_all_fields
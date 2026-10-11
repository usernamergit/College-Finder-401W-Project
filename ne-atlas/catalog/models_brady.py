# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Institution(models.Model):
    unit_id = models.IntegerField(primary_key=True)
    ope_id = models.CharField(max_length=10, blank=True, null=True)
    ope_id6 = models.CharField(max_length=10, blank=True, null=True)
    institution_name = models.CharField(max_length=255)
    city = models.CharField(max_length=120, blank=True, null=True)
    state_code = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    accrediting_agency = models.CharField(max_length=500, blank=True, null=True)
    institution_url = models.CharField(max_length=500, blank=True, null=True)
    net_price_calculator_url = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'institution'


class InstitutionSnapshot(models.Model):
    pk = models.CompositePrimaryKey('unit_id', 'release_id')
    unit = models.ForeignKey(Institution, models.DO_NOTHING)
    release = models.ForeignKey('SourceRelease', models.DO_NOTHING)
    main_campus = models.IntegerField(blank=True, null=True)
    branch_count = models.PositiveSmallIntegerField(blank=True, null=True)
    predominant_degree = models.PositiveIntegerField(blank=True, null=True)
    highest_degree = models.PositiveIntegerField(blank=True, null=True)
    control_type = models.PositiveIntegerField(blank=True, null=True)
    region_code = models.PositiveIntegerField(blank=True, null=True)
    locale_code = models.PositiveSmallIntegerField(blank=True, null=True)
    currently_operating = models.IntegerField(blank=True, null=True)
    distance_only = models.IntegerField(blank=True, null=True)
    undergraduate_enrollment = models.PositiveIntegerField(blank=True, null=True)
    admission_rate = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    average_sat = models.PositiveSmallIntegerField(blank=True, null=True)
    act_composite_midpoint = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    in_state_tuition = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    out_of_state_tuition = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    average_net_price_public = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    average_net_price_private = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    average_cost_of_attendance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    full_time_retention_4yr = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    full_time_retention_lt4yr = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    completion_rate_150_4yr = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    completion_rate_150_lt4yr = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    pell_recipient_rate = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    federal_loan_rate = models.DecimalField(max_digits=7, decimal_places=6, blank=True, null=True)
    median_debt_at_repayment = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    median_earnings_1yr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    median_earnings_4yr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    median_earnings_5yr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'institution_snapshot'


class ProgramSnapshot(models.Model):
    pk = models.CompositePrimaryKey('unit_id', 'cip_code', 'credential_level_id', 'release_id')
    unit = models.ForeignKey(Institution, models.DO_NOTHING)
    cip_code = models.ForeignKey('CipCode', models.DO_NOTHING, db_column='cip_code')
    credential_level = models.ForeignKey('CredentialLevel', models.DO_NOTHING)
    release = models.ForeignKey('SourceRelease', models.DO_NOTHING)
    awards_year_1 = models.PositiveIntegerField(blank=True, null=True)
    awards_year_2 = models.PositiveIntegerField(blank=True, null=True)
    borrower_count = models.PositiveIntegerField(blank=True, null=True)
    mean_debt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    median_debt = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    earners_count_1yr = models.PositiveIntegerField(blank=True, null=True)
    median_earnings_1yr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    earners_count_4yr = models.PositiveIntegerField(blank=True, null=True)
    median_earnings_4yr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    earners_count_5yr = models.PositiveIntegerField(blank=True, null=True)
    median_earnings_5yr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'program_snapshot'


class CipCode(models.Model):
    cip_code = models.CharField(primary_key=True, max_length=10)
    cip_display = models.CharField(max_length=12)
    cip_description = models.CharField(max_length=500)
    cip_version = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cip_code'


class CredentialLevel(models.Model):
    credential_level_id = models.PositiveIntegerField(primary_key=True)
    credential_description = models.CharField(max_length=160)

    class Meta:
        managed = False
        db_table = 'credential_level'


class SourceRelease(models.Model):
    release_id = models.CharField(primary_key=True, max_length=80)
    release_label = models.CharField(max_length=160)
    release_date = models.DateField()
    institution_academic_year = models.CharField(max_length=9, blank=True, null=True)
    program_academic_year = models.CharField(max_length=9, blank=True, null=True)
    source_name = models.CharField(max_length=120)
    source_url = models.CharField(max_length=500, blank=True, null=True)
    imported_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'source_release'

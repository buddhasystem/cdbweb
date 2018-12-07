# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppMessage(models.Model):
    app_message_id = models.AutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=5)
    message = models.TextField()
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'app_message'


class Basf2Module(models.Model):
    basf2_module_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    next_revision = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField()

    class Meta:
        managed = False
        db_table = 'basf2_module'


class GlobalTag(models.Model):
    global_tag_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    is_default = models.BooleanField()
    description = models.TextField(blank=True, null=True)
    global_tag_status = models.ForeignKey('GlobalTagStatus', models.DO_NOTHING)
    global_tag_type = models.ForeignKey('GlobalTagType', models.DO_NOTHING)
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField()

    class Meta:
        managed = False
        db_table = 'global_tag'


class GlobalTagPayload(models.Model):
    global_tag_payload_id = models.AutoField(primary_key=True)
    global_tag = models.ForeignKey(GlobalTag, models.DO_NOTHING)
    payload = models.ForeignKey('Payload', models.DO_NOTHING)
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'global_tag_payload'
        unique_together = (('global_tag', 'payload'),)


class GlobalTagPayload20180302Save(models.Model):
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    global_tag_id = models.IntegerField(blank=True, null=True)
    payload_id = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'global_tag_payload_20180302_save'


class GlobalTagStatus(models.Model):
    global_tag_status_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField()
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'global_tag_status'


class GlobalTagType(models.Model):
    global_tag_type_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'global_tag_type'


class GtpSave(models.Model):
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    global_tag_id = models.IntegerField(blank=True, null=True)
    payload_id = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gtp_save'


class GtpSave20170317(models.Model):
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    global_tag_id = models.IntegerField(blank=True, null=True)
    payload_id = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gtp_save_20170317'


class Payload(models.Model):
    payload_id = models.AutoField(primary_key=True)
    basf2_module = models.ForeignKey(Basf2Module, models.DO_NOTHING)
    revision = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField()
    base_url = models.TextField()
    payload_url = models.TextField()
    checksum = models.TextField()
    payload_status = models.ForeignKey('PayloadStatus', models.DO_NOTHING)
    deleted = models.BooleanField()
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField()

    class Meta:
        managed = False
        db_table = 'payload'
        unique_together = (('payload_id', 'revision'), ('basf2_module', 'revision'),)


class Payload20180302Save(models.Model):
    payload_id = models.IntegerField(blank=True, null=True)
    basf2_module_id = models.IntegerField(blank=True, null=True)
    revision = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(blank=True, null=True)
    base_url = models.TextField(blank=True, null=True)
    payload_url = models.TextField(blank=True, null=True)
    checksum = models.TextField(blank=True, null=True)
    payload_status_id = models.IntegerField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payload_20180302_save'


class PayloadContent(models.Model):
    payload_content_id = models.AutoField(primary_key=True)
    payload = models.ForeignKey(Payload, models.DO_NOTHING, unique=True, blank=True, null=True)
    content = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'payload_content'


class PayloadIov(models.Model):
    payload_iov_id = models.AutoField(primary_key=True)
    global_tag_payload = models.ForeignKey(GlobalTagPayload, models.DO_NOTHING)
    exp_start = models.IntegerField()
    run_start = models.IntegerField()
    exp_end = models.IntegerField()
    run_end = models.IntegerField()
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField()

    class Meta:
        managed = False
        db_table = 'payload_iov'
        unique_together = (('global_tag_payload', 'exp_start', 'run_start', 'exp_end', 'run_end'),)


class PayloadIov20180302Save(models.Model):
    payload_iov_id = models.IntegerField(blank=True, null=True)
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    exp_start = models.IntegerField(blank=True, null=True)
    run_start = models.IntegerField(blank=True, null=True)
    exp_end = models.IntegerField(blank=True, null=True)
    run_end = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)
    modified_by = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payload_iov_20180302_save'


class PayloadIovRpt(models.Model):
    payload_iov_rpt_id = models.AutoField(primary_key=True)
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)
    global_tag_id = models.IntegerField(blank=True, null=True)
    gt_name = models.TextField(blank=True, null=True)
    b2m_name = models.TextField(blank=True, null=True)
    exp_start = models.IntegerField(blank=True, null=True)
    exp_end = models.IntegerField(blank=True, null=True)
    run_start = models.IntegerField(blank=True, null=True)
    run_end = models.IntegerField(blank=True, null=True)
    payload_id = models.IntegerField(blank=True, null=True)
    payload_iov_id = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payload_iov_rpt'


class PayloadIovRpt20180302Save(models.Model):
    payload_iov_rpt_id = models.BigIntegerField(blank=True, null=True)
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True)
    dtm_mod = models.DateTimeField(blank=True, null=True)
    global_tag_id = models.IntegerField(blank=True, null=True)
    gt_name = models.TextField(blank=True, null=True)
    b2m_name = models.TextField(blank=True, null=True)
    exp_start = models.IntegerField(blank=True, null=True)
    exp_end = models.IntegerField(blank=True, null=True)
    run_start = models.IntegerField(blank=True, null=True)
    run_end = models.IntegerField(blank=True, null=True)
    payload_id = models.IntegerField(blank=True, null=True)
    payload_iov_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payload_iov_rpt_20180302_save'


class PayloadStatus(models.Model):
    payload_status_id = models.AutoField(primary_key=True)
    name = models.TextField(unique=True)
    description = models.TextField()
    dtm_ins = models.DateTimeField()
    dtm_mod = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'payload_status'

# commented out the models/tables which appear to exist in the dump
# but not in the initialization SQL script

from django.db import models


class AppMessage(models.Model):
    app_message_id = models.AutoField(primary_key=True, verbose_name="ID")
    code = models.CharField(unique=True, max_length=5)
    message = models.TextField()
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')

    class Meta:
        managed = False
        db_table = 'app_message'


class Basf2Module(models.Model):
    basf2_module_id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.TextField(unique=True)
    next_revision = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')
    modified_by = models.TextField(verbose_name='Modified by')

    class Meta:
        managed = False
        db_table = 'basf2_module'


class GlobalTag(models.Model):
    global_tag_id = models.AutoField(primary_key=True,  verbose_name="ID")
    name = models.TextField(unique=True)
    is_default = models.BooleanField(verbose_name='Default?')
    description = models.TextField(blank=True, null=True)
    
    global_tag_status_id = models.IntegerField(verbose_name='GT Status ID')
    # WAS auto-generated as:   global_tag_status = models.ForeignKey('GlobalTagStatus', models.DO_NOTHING)
    
    global_tag_type_id = models.IntegerField(verbose_name='GT Type ID')
    # WAS auto-generated as:    global_tag_type = models.ForeignKey('GlobalTagType', models.DO_NOTHING)
    
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')
    modified_by = models.TextField(verbose_name='Modified by')

    class Meta:
        managed = False
        db_table = 'global_tag'


class GlobalTagPayload(models.Model):
    global_tag_payload_id = models.AutoField(primary_key=True,  verbose_name="ID")
    
    global_tag_id = models.IntegerField(verbose_name='Global Tag ID')
    # WAS auto-generated as: global_tag = models.ForeignKey(GlobalTag, models.DO_NOTHING)
    
    payload_id = models.IntegerField(verbose_name='Payload ID')
    # WAS auto-generated as: payload = models.ForeignKey('Payload', models.DO_NOTHING)
    
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')

    class Meta:
        managed = False
        db_table = 'global_tag_payload'
        unique_together = (('global_tag_id', 'payload_id'),)


class GlobalTagStatus(models.Model):
    global_tag_status_id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.TextField(unique=True)
    description = models.TextField()
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')

    class Meta:
        managed = False
        db_table = 'global_tag_status'

class GlobalTagType(models.Model):
    global_tag_type_id = models.AutoField(primary_key=True,  verbose_name="ID")
    name = models.TextField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')

    class Meta:
        managed = False
        db_table = 'global_tag_type'

class Payload(models.Model):
    payload_id = models.AutoField(primary_key=True,  verbose_name="ID")
    
    basf2_module_id = models.IntegerField(verbose_name='BASF2 MODULE ID')
    # WAS auto-generated as: basf2_module = models.ForeignKey(Basf2Module, models.DO_NOTHING)
    
    revision = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(verbose_name='Default?')
    base_url = models.TextField()
    payload_url = models.TextField()
    checksum = models.TextField()
    
    payload_status_id = models.IntegerField(verbose_name='Status ID')
    # WAS auto-generated as: payload_status = models.ForeignKey('PayloadStatus', models.DO_NOTHING)
    
    deleted = models.BooleanField()
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')
    modified_by = models.TextField(verbose_name='Modified by')

    class Meta:
        managed = False
        db_table = 'payload'
        unique_together = (('payload_id', 'revision'), ('basf2_module_id', 'revision'),)


class PayloadIov(models.Model):
    payload_iov_id = models.AutoField(primary_key=True, verbose_name="ID")
    
    global_tag_payload_id = models.IntegerField(verbose_name='Global Tag Payload ID')
    # WAS auto-generated as: global_tag_payload = models.ForeignKey(GlobalTagPayload, models.DO_NOTHING)
    
    exp_start = models.IntegerField()
    run_start = models.IntegerField()
    exp_end = models.IntegerField()
    run_end = models.IntegerField()
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')
    modified_by = models.TextField(verbose_name='Modified by')

    class Meta:
        managed = False
        db_table = 'payload_iov'
        unique_together = (('global_tag_payload_id', 'exp_start', 'run_start', 'exp_end', 'run_end'),)


class PayloadIovRpt(models.Model):
    payload_iov_rpt_id = models.AutoField(primary_key=True)
    global_tag_payload_id = models.IntegerField(blank=True, null=True)
    dtm_ins = models.DateTimeField(blank=True, null=True, verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')
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

class PayloadStatus(models.Model):
    payload_status_id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.TextField(unique=True)
    description = models.TextField()
    dtm_ins = models.DateTimeField(verbose_name='Inserted')
    dtm_mod = models.DateTimeField(blank=True, null=True, verbose_name='Modified')

    class Meta:
        managed = False
        db_table = 'payload_status'

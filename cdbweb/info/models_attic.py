

# class GlobalTagPayload20180302Save(models.Model):
#     global_tag_payload_id = models.IntegerField(blank=True, null=True)
#     global_tag_id = models.IntegerField(blank=True, null=True)
#     payload_id = models.IntegerField(blank=True, null=True)
#     dtm_ins = models.DateTimeField(blank=True, null=True)
#     dtm_mod = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'global_tag_payload_20180302_save'


# class GtpSave(models.Model):
#     global_tag_payload_id = models.IntegerField(blank=True, null=True)
#     global_tag_id = models.IntegerField(blank=True, null=True)
#     payload_id = models.IntegerField(blank=True, null=True)
#     dtm_ins = models.DateTimeField(blank=True, null=True)
#     dtm_mod = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'gtp_save'


# class GtpSave20170317(models.Model):
#     global_tag_payload_id = models.IntegerField(blank=True, null=True)
#     global_tag_id = models.IntegerField(blank=True, null=True)
#     payload_id = models.IntegerField(blank=True, null=True)
#     dtm_ins = models.DateTimeField(blank=True, null=True)
#     dtm_mod = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'gtp_save_20170317'


# class Payload20180302Save(models.Model):
#     payload_id = models.IntegerField(blank=True, null=True)
#     basf2_module_id = models.IntegerField(blank=True, null=True)
#     revision = models.IntegerField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     is_default = models.BooleanField(blank=True, null=True)
#     base_url = models.TextField(blank=True, null=True)
#     payload_url = models.TextField(blank=True, null=True)
#     checksum = models.TextField(blank=True, null=True)
#     payload_status_id = models.IntegerField(blank=True, null=True)
#     deleted = models.BooleanField(blank=True, null=True)
#     dtm_ins = models.DateTimeField(blank=True, null=True)
#     dtm_mod = models.DateTimeField(blank=True, null=True)
#     modified_by = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'payload_20180302_save'


# class PayloadIov20180302Save(models.Model):
#     payload_iov_id = models.IntegerField(blank=True, null=True)
#     global_tag_payload_id = models.IntegerField(blank=True, null=True)
#     exp_start = models.IntegerField(blank=True, null=True)
#     run_start = models.IntegerField(blank=True, null=True)
#     exp_end = models.IntegerField(blank=True, null=True)
#     run_end = models.IntegerField(blank=True, null=True)
#     dtm_ins = models.DateTimeField(blank=True, null=True)
#     dtm_mod = models.DateTimeField(blank=True, null=True)
#     modified_by = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'payload_iov_20180302_save'


# class PayloadIovRpt20180302Save(models.Model):
#     payload_iov_rpt_id = models.BigIntegerField(blank=True, null=True)
#     global_tag_payload_id = models.IntegerField(blank=True, null=True)
#     dtm_ins = models.DateTimeField(blank=True, null=True)
#     dtm_mod = models.DateTimeField(blank=True, null=True)
#     global_tag_id = models.IntegerField(blank=True, null=True)
#     gt_name = models.TextField(blank=True, null=True)
#     b2m_name = models.TextField(blank=True, null=True)
#     exp_start = models.IntegerField(blank=True, null=True)
#     exp_end = models.IntegerField(blank=True, null=True)
#     run_start = models.IntegerField(blank=True, null=True)
#     run_end = models.IntegerField(blank=True, null=True)
#     payload_id = models.IntegerField(blank=True, null=True)
#     payload_iov_id = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'payload_iov_rpt_20180302_save'


# class PayloadContent(models.Model):
#     payload_content_id = models.AutoField(primary_key=True)
#     payload = models.ForeignKey(Payload, models.DO_NOTHING, unique=True, blank=True, null=True)
#     content = models.BinaryField()

#     class Meta:
#         managed = False
#         db_table = 'payload_content'



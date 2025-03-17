from django.db import models

from django.db import models

class MachineLog(models.Model):
    MACHINE_ID = models.IntegerField()
    LINE_NUMB = models.IntegerField()
    OPERATOR_ID = models.IntegerField()
    DATE = models.DateField()
    START_TIME = models.TimeField()
    END_TIME = models.TimeField()
    
    MODE = models.IntegerField()
    STITCH_COUNT = models.IntegerField()
    NEEDLE_RUNTIME = models.FloatField()
    NEEDLE_STOPTIME = models.FloatField()
    Tx_LOGID = models.IntegerField()
    Str_LOGID = models.IntegerField()
    DEVICE_ID = models.IntegerField()
    RESERVE = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('MACHINE_ID', 'OPERATOR_ID', 'START_TIME', 'END_TIME')
class MachineLog(models.Model):
    machine_id = models.IntegerField()
    line_numb = models.IntegerField()
    OPERATOR_ID = models.PositiveIntegerField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    login_time = models.TimeField()
    mode = models.IntegerField()
    stitch_count = models.IntegerField()
    needle_runtime = models.FloatField()
    needle_stoptime = models.FloatField()
    tx_logid = models.IntegerField()
    str_logid = models.IntegerField()
    device_id = models.IntegerField()
    reserve = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('machine_id', 'operator_id', 'start_time', 'end_time')

class DuplicateLog(models.Model):
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class ModeMessage(models.Model):
    mode = models.IntegerField(unique=True)
    message = models.TextField()

    def __str__(self):
        return f"Mode {self.mode}: {self.message}"

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
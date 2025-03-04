from django.db import models

class LogBase(models.Model):
    status_code = models.IntegerField()
    message = models.TextField()
    stack_trace = models.TextField(null=True, blank=True)
    request_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "log_base"
        verbose_name_plural = "log_base"
from django.db import models
from django.conf import settings

from datetime import datetime, timedelta

# Create your models here.

class Leave(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    applied_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    commencement_date = models.DateField()
    duration = models.IntegerField(blank=True)
    body = models.TextField()

    def __str__(self):
        return str(self.id) + ' - ' + str(self.user.name)
    
    def get_end_date(self):
        if not self.duration:
            return self.commencement_date
        return self.commencement_date + timedelta(days=self.duration-1)

    def save(self, *args, **kwargs):
        if self.is_approved and self.approved_date is None:
            self.approved_date = datetime.now().date()
        elif not self.is_approved and self.approved_date is not None:
            self.approved_date = None
        super(Leave, self).save(*args, **kwargs)
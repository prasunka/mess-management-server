from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.

class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    resolved = models.BooleanField(default=False)
    applied_date = models.DateField(auto_now_add=True)
    resolved_date = models.DateField(null=True, blank=True)

    def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'complaints/user_{0}_{1}/{2}'.format(instance.user.id, instance.user.name, filename)
    
    media = models.FileField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.resolved and self.resolved_date is None:
            self.resolved_date = datetime.now().date()
        elif not self.resolved and self.resolved_date is not None:
            self.resolved_date = None
        super(Complaint, self).save(*args, **kwargs)


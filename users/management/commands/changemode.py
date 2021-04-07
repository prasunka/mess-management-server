from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Changes the billing mode for all users according to their requested option'

    def handle(self, *args, **options):
        for user in get_user_model().objects.all():
            if (user.requestedBillingMode == user.billingMode):
                user.requestedBillingMode = None
                user.save()
                continue
            if user.requestedBillingMode is None:
                continue
            
            user.billingMode = user.requestedBillingMode
            user.requestedBillingMode = None
            user.save()
            self.stdout.write(self.style.SUCCESS("Successfully changed mode for user %d" % user.id))
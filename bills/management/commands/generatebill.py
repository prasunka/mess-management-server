from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from bills.models import Bill, BillGenerationHistory
from users.models import ModeHistory
from django.contrib.auth import get_user_model
from leaves.models import Leave
from django.db.models import F

class Command(BaseCommand):
    help = 'Generate bills for all users'

    def handle(self, *args, **options):
        today = datetime.now().date()
        today = today.replace(day=1)
        prev_month = today - timedelta(days=1)
        prev_month_first_day = (today - timedelta(days=1)).replace(day=1)

        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        generated = BillGenerationHistory.objects.order_by("-date")
        numBills = 0
        totalAmount = 0
        
        if not generated:
            self.stdout.write(self.style.WARNING("No previous generation history found."))
        
        else:
            last_gen = generated[0]
            if last_gen.date.month == prev_month.month:
                self.stdout.write("The bill for %s has already been generated." % prev_month.strftime("%B"))
                return
            else:
                self.stdout.write(self.style.WARNING("Generating bill for %s" % prev_month.strftime("%B")))

        for user in get_user_model().objects.filter(typeAccount='STUDENT'):
            modes = ModeHistory.objects.filter(user=user.id).order_by("-dateChanged")
            if not modes:
                mode = "MONTHLY"
            else:
                mode = modes[0].mode

            print(user.id, mode)
            if(mode=="COUPON"):
                continue

            leaves = Leave.objects.filter(user=user.id)\
                    .filter(is_approved=True)
            absent_duration = 0
       
            for date in daterange(prev_month_first_day, today):
                for leave in leaves:
                    if date>=leave.commencement_date and date <= leave.get_end_date():
                        absent_duration+=1
                        break
            
            month_duration = (prev_month - prev_month_first_day).days + 1
            duration = month_duration - absent_duration

            bill_amount = 120 * duration
            bill = Bill()
            bill.buyer = user
            bill.bill_amount = bill_amount
            bill.bill_from = prev_month_first_day
            bill.bill_days = duration
            bill.save()
            numBills += 1
            totalAmount += bill_amount
            self.stdout.write(self.style.SUCCESS("Bill generated for user %d" % user.id))
        
        gen = BillGenerationHistory(date=prev_month_first_day, numBills=numBills, totalAmount=totalAmount)
        gen.save()

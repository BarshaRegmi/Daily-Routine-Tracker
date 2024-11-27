from celery import shared_task
from .models import *
import datetime

@shared_task
def your_midnight_task():
    users = CustomUser.objects.all()
    
    for user in users:
        dayplan = DayPlan.objects.get(user = user, date = datetime.date.today())
        info = Info.objects.get(user = user)

        if dayplan.score > 0:
            new_av = info.discipline_score * info.total_active_days / (info.total_active_days + 1) + dayplan.score / (info.total_active_days + 1)
            info.discipline_score = new_av
            info.total_active_days += 1
            info.save()

        if dayplan.completed:
            continue
        else:
            info.streak = 0
            info.save()
    
    print("done")


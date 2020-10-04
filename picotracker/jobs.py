from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from django_apscheduler.jobstores import register_job
from django.core.management import call_command


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


every_3_hours_trigger = OrTrigger([
    CronTrigger(hour=hour)
    for hour in range(0, 24, 3)
])


@register_job(scheduler, every_3_hours_trigger)
def update_games():
    print('Starting: update_games')
    call_command('update_games')
    print('Done: update_games')


def start_scheduler():
    if scheduler.state == 0:
        register_events(scheduler)
        scheduler.start()
        print('Started scheduler.')
    else:
        print('Attempted to start scheduler, but scheduler was already running.')
from adlibre_tms.apps.quee.celery import celery
from adlibre_tms.apps.tms.models import RetainerRecurrence, Retainer, Timesheet, TimesheetRetainerAllocation
from datetime import datetime
from datetime import timedelta


# Test task for my debug
@celery.task
def add(x=None, y=None):
    if not x or not y:
        return 8
    print str(x+y)
    return x+y


@celery.task
def calculate_retainer():
    timesheets_counter = 0
    recurences = RetainerRecurrence.objects.all()
    for rec in recurences:
        start = datetime.combine(rec.start, datetime.min.time())
        end = datetime.combine(rec.end, datetime.min.time())
        # Timesheet for this time period and job, that is not allocated yet
        timesheets = Timesheet.objects.filter(
            job=rec.job,
            start_time__gt=start,
            end_time__lte=end,
            timesheetretainerallocation__timesheet=None
        )
        if timesheets:
            # We have timesheets. Starting calculation
            retainer = Retainer(
                job=rec.job,
                start=start,
                end=end,
                amount=rec.amount,
            )
            retainer.save()
            amount_used = timedelta(hours=0)
            now_month = datetime.now().month
            for timesheet in timesheets:
                timesheets_counter += 1
                t_date = datetime.combine(timesheet.start_time.date(), datetime.min.time())
                # because Retainer agreement could span for multiple months.
                if t_date.month == now_month:

                    tra = TimesheetRetainerAllocation(timesheet=timesheet, retainer=retainer)
                    # Actually calculating time of timesheet.
                    timesheet_time = timesheet.end_time - timesheet.start_time
                    amount_used += timesheet_time
                    tra.save()

            retainer.amount_used, remaind = divmod(amount_used.seconds, 3600)
            if (remaind / 60) > 30:
                retainer.amount_used += 1
            retainer.save()

    return 'Calculated time against retainer in %s timesheets.' % timesheets_counter
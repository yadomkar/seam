from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

@csrf_exempt
def create_polling_job(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('userId')
        api_endpoint = data.get('apiEndpoint')
        polling_interval = data.get('pollingInterval')  # Milliseconds

        # Convert milliseconds to seconds for the interval
        interval_seconds = polling_interval // 1000

        # Create or update the interval schedule
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=interval_seconds,
            period=IntervalSchedule.SECONDS,
        )

        # Create or update the periodic task
        task_name = f"Polling Task for User {user_id}"
        task, created = PeriodicTask.objects.get_or_create(
            name=task_name,
            defaults={
                'interval': schedule,
                'task': 'seam_app.tasks.poll_api_task',
                'args': json.dumps([api_endpoint, user_id]),
            }
        )

        if not created:
            # Update the task if it already exists
            task.interval = schedule
            task.args = json.dumps([api_endpoint, user_id])
            task.save()

        return JsonResponse({'message': 'Polling job created or updated successfully.'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

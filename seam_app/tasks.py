from celery import shared_task
import requests
import redis
from django.conf import settings
from .models import User

# Initialize a Redis connection
r = redis.Redis(host='redis', port=6379, db=0)


@shared_task
def poll_api_task(api_endpoint, user_id):
    print(f"Polling API for user {user_id}")
    response = requests.get(f"{api_endpoint}/{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        _ = user_data.pop('id', None)  # Remove the ID field from the data
        address_data = user_data.pop('address', {})

        # Prepare user data with address information
        user_data.update({
            'street': address_data.get('street'),
            'city': address_data.get('city'),
            'state': address_data.get('state'),
            'zipcode': address_data.get('zipcode'),
        })

        # Use a unique lock ID based on user_id
        lock_id = f"user_data_lock_{user_id}"
        with r.lock(lock_id, blocking_timeout=5) as lock:
            if lock:
                # Update or create the user record with new data
                User.objects.update_or_create(
                    user_id=user_id,
                    defaults=user_data
                )
                print(f"Processed data for user {user_id} successfully.")
            else:
                print(f"Skipped processing for user {user_id} due to lock not being acquired.")
    else:
        print(f"Failed to fetch data from {api_endpoint}")

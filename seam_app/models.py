from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_full_address(self):
        """Returns the combined address as a string."""
        address_parts = [self.street, self.city, self.state, self.zipcode]
        # Filter out any None values
        address_parts = [part for part in address_parts if part]
        return ', '.join(address_parts)

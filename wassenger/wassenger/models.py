from django.db import models

class Mensaje(models.Model):
    phone = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'{self.phone}: {self.message}'
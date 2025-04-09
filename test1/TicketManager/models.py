from django.db import models
from django.contrib.auth.models import AbstractUser


class RoleModel(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}---{self.name} '


class AuthUser(AbstractUser):
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE, related_name='users', null=True)

    def __str__(self):
        return self.username


# Create your models here.
class TicketManager(models.Model):
    ticketId = models.IntegerField(unique=True)
    issue = models.CharField(max_length=255)
    category = models.CharField(max_length=40)
    createdAt = models.DateField(auto_now_add=True)
    i3_priority = models.BooleanField(default=True)
    comments = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="New")
    clientId = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='tickets', db_column='client_id')
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE, related_name='tickets', db_column= 'role_id', null=True)

    def __str__(self):
        return f"The ticket {self.ticketId}: {self.issue}"

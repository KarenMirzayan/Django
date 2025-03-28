from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.category.name if self.category else 'No Category'}"


class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="group_expenses")

    @property
    def split_amount(self):
        num_users = self.users.count()
        return self.amount / num_users if num_users > 0 else 0

    def __str__(self):
        return f"{self.name} - {self.amount}"

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    HOD = "HOD"
    OFFICER = "OFFICER"
    ADMIN = "ADMIN"
    ROLE_CHOICES = [(HOD, "Head of Department"), (OFFICER, "Officer"), (ADMIN, "Administrator")]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")


class Category(models.Model):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=Category.TYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    receipt_ref = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="transactions")

    def __str__(self):
        return f"{self.transaction_type} {self.amount} on {self.date}"


class Budget(models.Model):
    month = models.DateField()
    amount_allocated = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="budgets")

    class Meta:
        unique_together = ("month", "category")


class Approval(models.Model):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    STATUS_CHOICES = [(PENDING, "Pending"), (APPROVED, "Approved"), (REJECTED, "Rejected")]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    decision_date = models.DateTimeField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="approval")
    decided_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="decisions")


class Setting(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=100)
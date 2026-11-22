from django import forms
from .models import Transaction, Budget, Approval


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["date", "amount", "transaction_type", "category", "description", "receipt_ref"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get("transaction_type")
        category = cleaned_data.get("category")
        if transaction_type and category and category.category_type != transaction_type:
            raise forms.ValidationError("The category type must match the transaction type.")
        return cleaned_data



class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["month", "category", "amount_allocated"]
        widgets = {
            "month": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_category(self):
        category = self.cleaned_data["category"]
        if category.category_type != "EXPENSE":
            raise forms.ValidationError("Budgets can only be set for expense categories.")
        return category


class ApprovalDecisionForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = ["status", "comment"]
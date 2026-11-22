from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .forms import TransactionForm, BudgetForm, ApprovalDecisionForm
from .models import Transaction, Budget, Category, Approval, Setting


@login_required
def record_transaction(request):
    if request.user.role.name != "OFFICER":
        return HttpResponseForbidden("Only an Officer can record transactions.")

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.recorded_by = request.user
            transaction.save()

            if transaction.transaction_type == "EXPENSE":
                limit_setting = Setting.objects.filter(name="approval_limit").first()
                limit = Decimal(limit_setting.value) if limit_setting else Decimal("0")
                if transaction.amount > limit:
                    Approval.objects.create(transaction=transaction)
                    messages.success(request, "Expense saved. It is over the limit and awaits approval.")
                else:
                    messages.success(request, "Transaction saved.")
            else:
                messages.success(request, "Transaction saved.")

            return redirect("record_transaction")
    else:
        form = TransactionForm()
    return render(request, "core/transaction_form.html", {"form": form})


@login_required
def dashboard(request):
    income_total = Transaction.objects.filter(transaction_type="INCOME").aggregate(total=Sum("amount"))["total"] or Decimal("0")
    expense_total = Transaction.objects.filter(transaction_type="EXPENSE").aggregate(total=Sum("amount"))["total"] or Decimal("0")
    balance = income_total - expense_total

    category_rows = []
    for category in Category.objects.filter(category_type="EXPENSE"):
        spent = Transaction.objects.filter(category=category, transaction_type="EXPENSE").aggregate(total=Sum("amount"))["total"] or Decimal("0")
        budget = Budget.objects.filter(category=category).order_by("-month").first()
        allocated = budget.amount_allocated if budget else Decimal("0")
        percent = int((spent / allocated) * 100) if allocated > 0 else 0
        category_rows.append({
            "name": category.name,
            "spent": spent,
            "allocated": allocated,
            "percent": min(percent, 100),
        })

    context = {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
        "category_rows": category_rows,
    }
    return render(request, "core/dashboard.html", context)


@login_required
def set_budget(request):
    if request.user.role.name != "OFFICER":
        return HttpResponseForbidden("Only an Officer can set budgets.")

    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget saved.")
            return redirect("set_budget")
    else:
        form = BudgetForm()

    budgets = Budget.objects.select_related("category").order_by("-month")
    return render(request, "core/budget_form.html", {"form": form, "budgets": budgets})


@login_required
def approvals_list(request):
    pending = Approval.objects.filter(status="PENDING").select_related("transaction")
    return render(request, "core/approvals_list.html", {"pending": pending})


@login_required
def decide_approval(request, approval_id):
    if request.user.role.name != "HOD":
        return HttpResponseForbidden("Only the Head of Department can decide an approval.")

    approval = Approval.objects.get(id=approval_id)
    if request.method == "POST":
        form = ApprovalDecisionForm(request.POST, instance=approval)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.decided_by = request.user
            decision.decision_date = timezone.now()
            decision.save()
            messages.success(request, "Decision saved.")
            return redirect("approvals_list")
    else:
        form = ApprovalDecisionForm(instance=approval)
    return render(request, "core/decide_approval.html", {"form": form, "approval": approval})


@login_required
def monthly_report(request):
    selected_month = request.GET.get("month")
    rows = []
    total_income = Decimal("0")
    total_expense = Decimal("0")

    if selected_month:
        year, month = selected_month.split("-")
        transactions = Transaction.objects.filter(date__year=year, date__month=month)
        for category in Category.objects.all():
            cat_transactions = transactions.filter(category=category)
            income = cat_transactions.filter(transaction_type="INCOME").aggregate(total=Sum("amount"))["total"] or Decimal("0")
            expense = cat_transactions.filter(transaction_type="EXPENSE").aggregate(total=Sum("amount"))["total"] or Decimal("0")
            if income or expense:
                rows.append({"category": category.name, "income": income, "expense": expense})
                total_income += income
                total_expense += expense

    context = {
        "rows": rows,
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "selected_month": selected_month,
    }
    return render(request, "core/monthly_report.html", context)
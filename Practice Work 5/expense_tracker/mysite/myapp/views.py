from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExpenseForm, CategoryForm, GroupExpenseForm
from .models import Expense, Category, GroupExpense
from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def index(request):
    expense_form = ExpenseForm()
    category_form = CategoryForm()
    group_expense_form = GroupExpenseForm()

    if request.method == "POST":
        if 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                expense.save()
                return redirect('index')

        elif 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('index')

        elif 'add_group_expense' in request.POST:
            group_expense_form = GroupExpenseForm(request.POST)
            if group_expense_form.is_valid():
                group_expense = group_expense_form.save(commit=False)
                group_expense.save()
                users = group_expense_form.cleaned_data["users"] | User.objects.filter(id=request.user.id)
                group_expense.users.set(users)

                return redirect("index")
            else:
                group_expense_form = GroupExpenseForm()

    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.all()
    group_expenses = GroupExpense.objects.filter(users=request.user)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category_id = request.GET.get('category')

    if start_date:
        expenses = expenses.filter(date__gte=start_date)
        group_expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)
        group_expenses = expenses.filter(date__lte=end_date)
    if category_id:
        expenses = expenses.filter(category_id=category_id)
        group_expenses = expenses.filter(category_id=category_id)

    total_expenses = expenses.aggregate(Sum('amount'))
    total_group_expenses = group_expenses.aggregate(Sum('amount'))

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_week = datetime.date.today() - datetime.timedelta(days=7)

    yearly_sum = expenses.filter(date__gt=last_year).aggregate(Sum("amount")).get("amount__sum", 0) or 0
    monthly_sum = expenses.filter(date__gt=last_month).aggregate(Sum("amount")).get("amount__sum", 0) or 0
    weekly_sum = expenses.filter(date__gt=last_week).aggregate(Sum("amount")).get("amount__sum", 0) or 0

    def calculate_split_total(queryset):
        total = 0
        for expense in queryset:
            total += expense.split_amount
        return total

    yearly_group_expenses = group_expenses.filter(date__gt=last_year)
    monthly_group_expenses = group_expenses.filter(date__gt=last_month)
    weekly_group_expenses = group_expenses.filter(date__gt=last_week)

    yearly_group_sum = calculate_split_total(yearly_group_expenses)
    monthly_group_sum = calculate_split_total(monthly_group_expenses)
    weekly_group_sum = calculate_split_total(weekly_group_expenses)

    total_yearly_sum = yearly_sum + yearly_group_sum
    total_monthly_sum = monthly_sum + monthly_group_sum
    total_weekly_sum = weekly_sum + weekly_group_sum

    daily_sums = expenses.values('date').order_by('date').annotate(sum=Sum('amount'))
    group_daily_sums = expenses.values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = (
        expenses
        .filter(category__isnull=False)
        .values('category__name')
        .annotate(sum=Sum('amount'))
        .order_by('-sum')
    )
    group_categorical_sums = (
        group_expenses
        .filter(category__isnull=False)
        .values('category__name')
        .annotate(sum=Sum('amount'))
        .order_by('-sum')
    )

    return render(
        request,
        'myapp/index.html',
        {
            'expense_form': expense_form,
            'category_form': category_form,
            'expenses': expenses,
            'categories': categories,
            'total_expenses': total_expenses,
            'yearly_sum': yearly_sum,
            'monthly_sum': monthly_sum,
            'weekly_sum': weekly_sum,
            'daily_sums': daily_sums,
            'categorical_sums': categorical_sums,
            'group_expense_form': group_expense_form,
            'group_expenses': group_expenses,
            'total_group_expenses': total_group_expenses,
            'total_yearly_sum': total_yearly_sum,
            'total_monthly_sum': total_monthly_sum,
            'total_weekly_sum': total_weekly_sum,
            'group_daily_sums': group_daily_sums,
            'group_categorical_sums': group_categorical_sums,
        }
    )


@login_required
def edit(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense_form = ExpenseForm(instance=expense)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'myapp/edit.html', {'expense_form': expense_form})


@login_required
def edit_group_expense(request, id):
    group_expense = get_object_or_404(GroupExpense, id=id, users=request.user)  # Only allow participants to edit
    group_expense_form = GroupExpenseForm(instance=group_expense)

    if request.method == "POST":
        form = GroupExpenseForm(request.POST, instance=group_expense)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the main page after editing

    return render(request, 'myapp/edit_group_expense.html', {'group_expense_form': group_expense_form})


@login_required
def delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST" and 'delete' in request.POST:
        expense.delete()
    return redirect('index')


@login_required
def delete_group_expense(request, id):
    expense = get_object_or_404(GroupExpense, id=id, users=request.user)
    if request.method == "POST" and 'delete' in request.POST:
        expense.delete()
    return redirect('index')

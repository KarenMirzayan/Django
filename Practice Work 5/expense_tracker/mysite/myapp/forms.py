from django import forms
from .models import Expense, Category, GroupExpense
from django.contrib.auth import get_user_model

User = get_user_model()


class ExpenseForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select Category"
    )

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter new category'})
        }


class GroupExpenseForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = GroupExpense
        fields = ['name', 'amount', 'category', 'users']

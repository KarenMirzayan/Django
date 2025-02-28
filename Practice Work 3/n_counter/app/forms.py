from django import forms
from .models import HealthGoal, Food

class HealthGoalForm(forms.ModelForm):
    class Meta:
        model = HealthGoal
        fields = ['daily_calorie_goal', 'carb_goal', 'protein_goal', 'fat_goal']
        labels = {
            'daily_calorie_goal': 'Daily Calorie Goal (kcal)',
            'carb_goal': 'Carbohydrate Goal (g)',
            'protein_goal': 'Protein Goal (g)',
            'fat_goal': 'Fat Goal (g)',
        }
        widgets = {
            'daily_calorie_goal': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'carb_goal': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'protein_goal': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'fat_goal': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ["name", "carbs", "proteins", "fats", "calories"]

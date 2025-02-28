from django.shortcuts import render, redirect
from .models import Food

from django.shortcuts import render
from .models import Food, Consume, HealthGoal

from django.http import JsonResponse
from .forms import HealthGoalForm

from django.db.models import Sum
import datetime

from django.contrib.auth.forms import UserCreationForm
from .forms import FoodForm

def index(request):
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        user = request.user
        consume = Consume(user=user, food_consumed=consume)
        consume.save()

    foods = Food.objects.all()
    consumed_food = Consume.objects.filter(user=request.user)
    health_goal, _ = HealthGoal.objects.get_or_create(user=request.user)

    return render(request, 'app/index.html', {
        'foods': foods,
        'consumed_food': consumed_food,
        'health_goal': health_goal
    })


def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'app/delete.html')

def nutrient_data_by_time(request):
    user = request.user
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    consumed_today = Consume.objects.filter(user=user, date=today)
    consumed_week = Consume.objects.filter(user=user, date__gte=week_start)
    consumed_month = Consume.objects.filter(user=user, date__gte=month_start)

    def aggregate_nutrients(queryset):
        return {
            "calories": queryset.aggregate(Sum('food_consumed__calories'))['food_consumed__calories__sum'] or 0,
            "carbs": queryset.aggregate(Sum('food_consumed__carbs'))['food_consumed__carbs__sum'] or 0,
            "proteins": queryset.aggregate(Sum('food_consumed__proteins'))['food_consumed__proteins__sum'] or 0,
            "fats": queryset.aggregate(Sum('food_consumed__fats'))['food_consumed__fats__sum'] or 0
        }

    data = {
        "daily": aggregate_nutrients(consumed_today),
        "weekly": aggregate_nutrients(consumed_week),
        "monthly": aggregate_nutrients(consumed_month),
    }

    return JsonResponse(data)

def set_goals(request):
    user = request.user
    goal, created = HealthGoal.objects.get_or_create(user=user)

    if request.method == "POST":
        form = HealthGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = HealthGoalForm(instance=goal)

    return render(request, 'app/set_goals.html', {'form': form})

def nutrient_data(request):
    consumed = Consume.objects.filter(user=request.user)
    data = {
        "carbs": sum(c.food_consumed.carbs for c in consumed),
        "proteins": sum(c.food_consumed.proteins for c in consumed),
        "fats": sum(c.food_consumed.fats for c in consumed),
        "calories": sum(c.food_consumed.calories for c in consumed),
    }
    return JsonResponse(data)

def chart_data(request):
    consumed = Consume.objects.filter(user=request.user)
    data = {
        "labels": [c.food_consumed.name for c in consumed],
        "carbs": [c.food_consumed.carbs for c in consumed],
        "proteins": [c.food_consumed.proteins for c in consumed],
        "fats": [c.food_consumed.fats for c in consumed],
        "calories": [c.food_consumed.calories for c in consumed],
    }
    return JsonResponse(data)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "app/register.html", {"form": form})

def add_food(request):
    if request.method == "POST":
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = FoodForm()
    return render(request, "app/add_food.html", {"form": form})

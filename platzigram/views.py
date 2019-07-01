"""Platzigram views."""

from django.http import HttpResponse, JsonResponse
from django.utils import timezone


def hello_world(request):
    """Return a greeting."""
    now = timezone.now().strftime('%b %dth, %Y - %H:%M hrs')
    msg = 'Oh hi? Current server time is {now}'.format(now=now)
    return HttpResponse(msg)


def sort_numbers(request):
    """Return a JSON response with sorted integers."""
    numbers = request.GET.get('numbers', None)
    numbers = list(map(int, numbers.split(','))) if numbers else []
    sorted_numbers = sorted(numbers)
    response = {
        'numbers': numbers,
        'sorted_numbers': sorted_numbers
    }
    return JsonResponse(response)


def say_hi(request, name, age):
    """Return a greeting."""
    if age < 12:
        msg = 'Sorry {} you are not allowed here.'.format(name)
    else:
        msg = 'Hello, {}! Welcome to Platzigram'.format(name)
    return HttpResponse(msg)

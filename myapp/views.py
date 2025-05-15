from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Quantity
from django.utils.dateparse import parse_date
import paho.mqtt.client as mqtt


@csrf_exempt
def quantity_api(request):
    print("Method:", request.method)
    print("Raw Body:", request.body)

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            quantity_val = body.get('quantity', '')

            if not quantity_val:
                return JsonResponse({'error': 'Missing "quantity" field.'}, status=400)

            # Save the quantity (as string)
            Quantity.objects.create(quantity=quantity_val)

            # Return all entries
            all_data = Quantity.objects.all().order_by('date', 'time')
            result = [
                {
                    'date': data.date.isoformat(),
                    'time': data.time.strftime('%H:%M'),
                    'quantity': data.quantity
                }
                for data in all_data
            ]
            return JsonResponse(result, safe=False, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        all_data = Quantity.objects.all().order_by('date', 'time')
        result = [
            {
                'date': data.date.isoformat(),
                'time': data.time.strftime('%H:%M'),
                'quantity': data.quantity
            }
            for data in all_data
        ]
        return JsonResponse(result, safe=False)

    return JsonResponse({'error': 'Only GET and POST allowed'}, status=405)


@csrf_exempt
def filter_quantities(request):
    if request.method == 'GET':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # Check if both dates are provided
        if not from_date or not to_date:
            return JsonResponse({'error': 'from_date and to_date are required.'}, status=400)

        # Parse the dates
        parsed_from = parse_date(from_date)
        parsed_to = parse_date(to_date)

        # Validate parsed dates
        if not parsed_from or not parsed_to:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        # Check if from_date is after to_date
        if parsed_from > parsed_to:
            return JsonResponse({'error': 'from_date cannot be after to_date.'}, status=400)

        # Filter the data
        entries = Quantity.objects.filter(date__range=(parsed_from, parsed_to))
        
        result = [
            {
                'date': data.date.isoformat(),
                'time': data.time.strftime('%H:%M'),
                'quantity': data.quantity
            }
            for data in entries.order_by('date', 'time')
        ]

        return JsonResponse(result, safe=False)

    return JsonResponse({'error': 'Only GET method allowed'}, status=405)
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # import json

# # # In-memory storage (reset every server restart) 
# # message_store = []

# # @csrf_exempt
# # def message_api(request):
# #     print("Method:", request.method)
# #     print("Raw Body:", request.body)

# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             print("Parsed JSON:", data)

# #             date = data.get('date')
# #             time = data.get('time')
# #             message = data.get('message')

# #             if not all([date, time, message]):
# #                 return JsonResponse(
# #                     {'error': 'date, time, and message are required'},
# #                     status=400
# #                 )

# #             new_message = {
# #                 'date': date,
# #                 'time': time,
# #                 'message': message
# #             }
# #             message_store.append(new_message)

# #             return JsonResponse({'success': True, 'data': new_message}, status=201)

# #         except json.JSONDecodeError:
# #             return JsonResponse({'error': 'Invalid JSON'}, status=400)

# #     elif request.method == 'GET':
# #         return JsonResponse({'messages': message_store}, status=200)

# #     else:
# #         return JsonResponse({'error': 'Method not allowed'}, status=405)




# #by using model store data############

# import json
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from .models import Message
# from django.utils.dateparse import parse_date, parse_time

# @csrf_exempt
# def message_api(request):
#     print("Method:", request.method)
#     print("Raw Body:", request.body)

#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body)
#             date = parse_date(body.get('date'))
#             time = parse_time(body.get('time'))
#             message_text = body.get('message', '')

#             # Save the message
#             Message.objects.create(date=date, time=time, message=message_text)

#             # Return all messages after saving
#             messages = Message.objects.all().order_by('date', 'time')
#             result = [
#                 {
#                     'date': data.date,
#                     'time': data.time,
#                     'message': data.message
#                 }
#                 for data in messages
#             ]
#             return JsonResponse(result, safe=False, status=201)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     elif request.method == 'GET':
#         messages = Message.objects.all().order_by('date', 'time')
#         result = [
#             {
#                 'date': data.date,
#                 'time': data.time,
#                 'message': data.message
#             }
#             for data in messages
#         ]
#         return JsonResponse(result, safe=False)

#     return JsonResponse({'error': 'Only GET and POST allowed'}, status=405)

# @csrf_exempt
# def filter_messages(request):
#     if request.method == 'GET':
#         date = request.GET.get('date')  
#         messages = Message.objects.all()

#         if date:
#             parsed_date = parse_date(date)
#             if parsed_date:
#                 messages = messages.filter(date=parsed_date)

#         result = [
#             {
#                 'date': data.date,
#                 'time': data.time,
#                 'message': data.message
#             }
#             for data in messages.order_by('date', 'time')
#         ]
#         return JsonResponse(result, safe=False)

#     return JsonResponse({'error': 'Only GET method allowed'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Quantity
from django.utils.dateparse import parse_date

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


# @csrf_exempt
# def filter_quantities(request):
#     if request.method == 'GET':
#         date = request.GET.get('date')  
#         entries = Quantity.objects.all()

#         if date:
#             parsed_date = parse_date(date)
#             if parsed_date:
#                 entries = entries.filter(date=parsed_date)

#         result = [
#             {
#                 'date': data.date.isoformat(),
#                 'time': data.time.strftime('%H:%M:%S'),
#                 'quantity': data.quantity
#             }
#             for data in entries.order_by('date', 'time')
#         ]
#         return JsonResponse(result, safe=False)

#     return JsonResponse({'error': 'Only GET method allowed'}, status=405)

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

        # Format the results
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
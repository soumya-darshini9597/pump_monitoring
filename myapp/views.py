# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# # In-memory storage (reset every server restart) 
# message_store = []

# @csrf_exempt
# def message_api(request):
#     print("Method:", request.method)
#     print("Raw Body:", request.body)

#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print("Parsed JSON:", data)

#             date = data.get('date')
#             time = data.get('time')
#             message = data.get('message')

#             if not all([date, time, message]):
#                 return JsonResponse(
#                     {'error': 'date, time, and message are required'},
#                     status=400
#                 )

#             new_message = {
#                 'date': date,
#                 'time': time,
#                 'message': message
#             }
#             message_store.append(new_message)

#             return JsonResponse({'success': True, 'data': new_message}, status=201)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)

#     elif request.method == 'GET':
#         return JsonResponse({'messages': message_store}, status=200)

#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)




#by using model store data############

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Message
from django.utils.dateparse import parse_date, parse_time

@csrf_exempt
def message_api(request):
    print("Method:", request.method)
    print("Raw Body:", request.body)

    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            date = parse_date(body.get('date'))
            time = parse_time(body.get('time'))
            message_text = body.get('message', '')

            # Save the message
            Message.objects.create(date=date, time=time, message=message_text)

            # Return all messages after saving
            messages = Message.objects.all().order_by('date', 'time')
            result = [
                {
                    'date': data.date,
                    'time': data.time,
                    'message': data.message
                }
                for data in messages
            ]
            return JsonResponse(result, safe=False, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        messages = Message.objects.all().order_by('date', 'time')
        result = [
            {
                'date': data.date,
                'time': data.time,
                'message': data.message
            }
            for data in messages
        ]
        return JsonResponse(result, safe=False)

    return JsonResponse({'error': 'Only GET and POST allowed'}, status=405)

@csrf_exempt
def filter_messages(request):
    if request.method == 'GET':
        date = request.GET.get('date')  
        messages = Message.objects.all()

        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                messages = messages.filter(date=parsed_date)

        result = [
            {
                'date': data.date,
                'time': data.time,
                'message': data.message
            }
            for data in messages.order_by('date', 'time')
        ]
        return JsonResponse(result, safe=False)

    return JsonResponse({'error': 'Only GET method allowed'}, status=405)
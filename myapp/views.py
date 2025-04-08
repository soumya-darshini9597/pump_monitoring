from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# In-memory storage (reset every server restart)
message_store = []

@csrf_exempt
def message_api(request):
    print("Method:", request.method)
    print("Raw Body:", request.body)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Parsed JSON:", data)

            date = data.get('date')
            time = data.get('time')
            message = data.get('message')

            if not all([date, time, message]):
                return JsonResponse(
                    {'error': 'date, time, and message are required'},
                    status=400
                )

            new_message = {
                'date': date,
                'time': time,
                'message': message
            }
            message_store.append(new_message)

            return JsonResponse({'success': True, 'data': new_message}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    elif request.method == 'GET':
        return JsonResponse({'messages': message_store}, status=200)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


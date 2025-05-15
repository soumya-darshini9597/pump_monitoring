from django.core.management.base import BaseCommand
from myapp.pahomqtt import mqtt_connect

class Command(BaseCommand):
    help = 'Starts MQTT subscriber'

    def handle(self, *args, **kwargs):
        print("Starting MQTT Subscriber...")
        mqtt_connect()




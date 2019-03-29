import requests
from django.conf import settings


def forward_event(channel, event, data):
    """Forward the event message through the server"""
    forward_url = f'{settings.BASE_URL}/forward-event/'
    requests.post(forward_url, json={
        'channel': channel, 'event': event, 'data': data})

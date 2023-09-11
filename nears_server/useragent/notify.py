from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from channels.layers import get_channel_layer
from stream.consumers import messageConsumer

from rest_server.models import Case




# async def alert_agent(channel_name, message):
#     channel_layer = get_channel_layer()
#     consumer = messageConsumer()
#     await channel_layer.send(channel_name, {
#         "type": "chat_message",
#         "message": message
#     })


# @receiver(pre_save, sender=Case)
# def assigned_agent(sender, instance, **kwargs):
#     # Check if the specific field has been updated
#     print("Prepare the email message")
#     if kwargs['update_fields'] and 'received_by' in kwargs['update_fields']:
        
#         print(kwargs['update_fields'])
#         print("Prepare the email message")
#         # Prepare the email message
#         # alert_agent("channel_name", "message")
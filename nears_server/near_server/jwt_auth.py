from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async
 
 
class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """
 
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner
 
    async def __call__(self, scope, receive, send):
 
        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
 
        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        
            user = await sync_to_async(get_user_model().objects.get)(id=decoded_data["user_id"])
            scope['user'] = user
 
        # Call close_old_connections using sync_to_async
        await sync_to_async(close_old_connections)()
 
        # Return the inner application directly and let it run everything else
        await self.inner(scope, receive, send)
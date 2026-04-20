from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from urllib.parse import parse_qs
import logging

from apps.users.models import User

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # close any old db connections
        close_old_connections()

        # extract query params
        query_string = scope.get('query_string' , b'').decode()

        # parse it into dict
        params = parse_qs(query_string)

        # extract token
        token = params.get('token' , [None])[0]

        # if no token provided then the user will be treated as anonymous
        scope['user'] = AnonymousUser()

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token.get('user_id')
                logger.info(f"JWT: Attempting to authenticate user {user_id}")
                user = await self.get_user_from_db(user_id)

                if user:
                    scope['user'] = user
                    logger.info(f"JWT: Successfully authenticated user {user_id}")
                else:
                    logger.warning(f"JWT: User {user_id} not found in database")
            except TokenError as e:
                logger.error(f"JWT TokenError: {e}")
            except Exception as e:
                logger.error(f"JWT Exception: {e}")



        return await super().__call__(scope, receive, send)
    

    @database_sync_to_async
    def get_user_from_db(self , user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

from datetime import timedelta

from django.conf import settings


JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_HOURS = 24
JWT_ACCESS_TOKEN_EXPIRE_DELTA = timedelta(hours=JWT_ACCESS_TOKEN_EXPIRE_HOURS)
JWT_SECRET_KEY = settings.SECRET_KEY
JWT_AUTH_HEADER_PREFIX = "Bearer"

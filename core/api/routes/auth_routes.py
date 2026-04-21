import json

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pydantic import ValidationError
from rest_framework.decorators import api_view

from core.schemas.auth import GoogleLoginRequest
from core.services.auth_service import AuthService


service = AuthService()


@swagger_auto_schema(
    method="post",
    operation_summary="Login con Google SSO",
    operation_description="Recibe un token de Google y retorna un JWT para acceder a los endpoints protegidos.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["token"],
        properties={
            "token": openapi.Schema(type=openapi.TYPE_STRING, description="Token de Google OAuth2"),
        },
    ),
    responses={
        200: openapi.Response("JWT generado exitosamente"),
        401: openapi.Response("Token de Google inválido"),
    },
)
@api_view(["POST"])
def google_login(request):
    try:
        body = json.loads(request.body or "{}")
        payload = GoogleLoginRequest(**body)

        response = service.login_with_google(payload.token)
        return JsonResponse(response.model_dump(mode="json"), status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)
    except ValidationError as exc:
        return JsonResponse({"error": exc.errors()}, status=422)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=401)
    except Exception as exc:
        print("GOOGLE LOGIN ERROR:", repr(exc))
        return JsonResponse({"error": str(exc)}, status=400)

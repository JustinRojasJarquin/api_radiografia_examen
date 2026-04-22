import jwt
from django.http import HttpResponseRedirect, JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from core.settings.security import verify_signed_image_token


@swagger_auto_schema(
    method="get",
    operation_summary="Ver imagen con URL firmada",
    operation_description="Redirige a la imagen en Cloudinary si el token firmado es válido. El token expira en 5 minutos.",
    manual_parameters=[
        openapi.Parameter("token", openapi.IN_QUERY, description="Token JWT firmado", type=openapi.TYPE_STRING, required=True),
    ],
    responses={
        302: openapi.Response("Redirección a la imagen en Cloudinary"),
        400: openapi.Response("Token inválido o faltante"),
        401: openapi.Response("Token expirado"),
    },
)
@api_view(["GET"])
def view_signed_image(request):
    token = request.GET.get("token")
    if not token:
        return JsonResponse({"error": "Missing token"}, status=400)

    try:
        payload = verify_signed_image_token(token)
        image_url = payload["image_url"]

        return HttpResponseRedirect(image_url)

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Signed URL expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid signed URL"}, status=401)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)

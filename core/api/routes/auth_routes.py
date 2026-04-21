import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError

from core.schemas.auth import GoogleLoginRequest
from core.services.auth_service import AuthService


service = AuthService()


@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

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

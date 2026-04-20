import jwt
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.settings.security import verify_signed_image_token


@csrf_exempt
def view_signed_image(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

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
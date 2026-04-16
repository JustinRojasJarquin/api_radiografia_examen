import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.database.session import SessionLocal
from core.schemas.radiography_record import (
    RadiographyRecordCreate,
    RadiographyRecordResponse,
    RadiographyRecordUpdate,
)
from core.services.radiography_record_service import RadiographyRecordService


service = RadiographyRecordService()


@csrf_exempt
def radiography_record_list_create(request):
    db = SessionLocal()

    try:
        if request.method == "GET":
            records = service.list_records(db)
            data = [
                RadiographyRecordResponse.model_validate(record).model_dump(mode="json")
                for record in records
            ]
            return JsonResponse(data, safe=False, status=200)

        if request.method == "POST":
            body = json.loads(request.body)
            payload = RadiographyRecordCreate(**body)

            record = service.create_record(db, payload)
            data = RadiographyRecordResponse.model_validate(record).model_dump(mode="json")
            return JsonResponse(data, status=201)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=404)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    finally:
        db.close()


@csrf_exempt
def radiography_record_detail(request, record_id: int):
    db = SessionLocal()

    try:
        if request.method == "GET":
            record = service.get_record_detail(db, record_id)
            data = RadiographyRecordResponse.model_validate(record).model_dump(mode="json")
            return JsonResponse(data, status=200)

        if request.method == "PUT":
            body = json.loads(request.body)
            payload = RadiographyRecordUpdate(**body)

            updated_record = service.update_record(db, record_id, payload)
            data = RadiographyRecordResponse.model_validate(updated_record).model_dump(mode="json")
            return JsonResponse(data, status=200)

        if request.method == "DELETE":
            result = service.delete_record(db, record_id)
            return JsonResponse(result, status=200)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=404)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    finally:
        db.close()
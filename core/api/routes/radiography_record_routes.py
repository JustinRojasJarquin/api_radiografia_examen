import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.api.dependencies import require_authenticated_user
from core.database.session import SessionLocal
from core.schemas.radiography_record import (
    RadiographyRecordCreate,
    RadiographyRecordResponse,
    RadiographyRecordUpdate,
)
from core.services.radiography_record_service import RadiographyRecordService
from core.services.file_service import process_and_upload_image
from core.utils.exceptions import AuthenticationException
from core.utils.pagination import get_pagination_params
from core.utils.filters import apply_record_filters
from core.database.models.radiography_record import RadiographyRecord


service = RadiographyRecordService()


@csrf_exempt
def radiography_record_list_create(request):
    db = SessionLocal()

    try:
        user = require_authenticated_user(request)

        if request.method == "GET":
            params = dict(request.GET)
            params = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}

            page, page_size = get_pagination_params(params)
            query = db.query(RadiographyRecord)
            query = apply_record_filters(query, RadiographyRecord, params)

            total = query.count()
            records = query.offset((page - 1) * page_size).limit(page_size).all()

            data = [
                RadiographyRecordResponse.model_validate(r).model_dump(mode="json")
                for r in records
            ]
            return JsonResponse({
                "total": total,
                "page": page,
                "page_size": page_size,
                "results": data,
            }, status=200)

        if request.method == "POST":
            image_file = request.FILES.get("image")
            if not image_file:
                return JsonResponse({"error": "Se requiere una imagen"}, status=400)

            upload_result = process_and_upload_image(image_file)

            payload = RadiographyRecordCreate(
                patient_full_name=request.POST.get("patient_full_name"),
                patient_identifier=request.POST.get("patient_identifier"),
                clinical_reference=request.POST.get("clinical_reference"),
                study_date=request.POST.get("study_date"),
                created_by=user.id,
                image_url=upload_result["url"],
                image_public_id=upload_result["public_id"],
            )

            record = service.create_record(db, payload)
            data = RadiographyRecordResponse.model_validate(record).model_dump(mode="json")
            return JsonResponse(data, status=201)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    except AuthenticationException as exc:
        return JsonResponse({"error": str(exc)}, status=401)
    except ValidationError as exc:
        return JsonResponse({"error": exc.message}, status=400)
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
        require_authenticated_user(request)

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

    except AuthenticationException as exc:
        return JsonResponse({"error": str(exc)}, status=401)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=404)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    finally:
        db.close()

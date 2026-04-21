import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from core.api.dependencies import require_authenticated_user
from core.database.session import SessionLocal
from core.schemas.radiography_record import (
    RadiographyRecordCreate,
    RadiographyRecordResponse,
    RadiographyRecordUpdate,
)
from core.services.radiography_record_service import RadiographyRecordService
from core.services.file_service import process_and_upload_image, generate_signed_image_url
from core.utils.exceptions import AuthenticationException
from core.utils.pagination import get_pagination_params
from core.utils.filters import apply_record_filters
from core.database.models.radiography_record import RadiographyRecord

service = RadiographyRecordService()


@swagger_auto_schema(
    method="get",
    operation_summary="Listar registros radiográficos",
    operation_description="Retorna lista paginada de registros. Soporta filtros por nombre, identificación, fecha y búsqueda general.",
    manual_parameters=[
        openapi.Parameter("page", openapi.IN_QUERY, description="Número de página", type=openapi.TYPE_INTEGER),
        openapi.Parameter("page_size", openapi.IN_QUERY, description="Registros por página (máx 100)", type=openapi.TYPE_INTEGER),
        openapi.Parameter("patient_full_name", openapi.IN_QUERY, description="Filtrar por nombre del paciente", type=openapi.TYPE_STRING),
        openapi.Parameter("patient_identifier", openapi.IN_QUERY, description="Filtrar por número de identificación", type=openapi.TYPE_STRING),
        openapi.Parameter("study_date", openapi.IN_QUERY, description="Filtrar por fecha (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        openapi.Parameter("search", openapi.IN_QUERY, description="Búsqueda general en nombre, id y referencia", type=openapi.TYPE_STRING),
        openapi.Parameter("order_by", openapi.IN_QUERY, description="Ordenar por campo (ej: study_date o -study_date)", type=openapi.TYPE_STRING),
    ],
    responses={200: openapi.Response("Lista paginada de registros"), 401: openapi.Response("No autenticado")},
)
@swagger_auto_schema(
    method="post",
    operation_summary="Crear registro radiográfico",
    operation_description="Crea un nuevo registro subiendo la imagen a Cloudinary via multipart/form-data.",
    manual_parameters=[
        openapi.Parameter("patient_full_name", openapi.IN_FORM, description="Nombre completo del paciente", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter("patient_identifier", openapi.IN_FORM, description="Número de identificación o historia clínica", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter("clinical_reference", openapi.IN_FORM, description="Referencia clínica breve", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter("study_date", openapi.IN_FORM, description="Fecha del estudio (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter("image", openapi.IN_FORM, description="Imagen radiográfica (jpeg/png/webp/gif, máx 5MB)", type=openapi.TYPE_FILE, required=True),
    ],
    consumes=["multipart/form-data"],
    responses={201: openapi.Response("Registro creado"), 400: openapi.Response("Datos inválidos"), 401: openapi.Response("No autenticado")},
)
@api_view(["GET", "POST"])
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


@swagger_auto_schema(
    method="get",
    operation_summary="Detalle de un registro",
    responses={200: openapi.Response("Registro encontrado"), 401: openapi.Response("No autenticado"), 404: openapi.Response("No encontrado")},
)
@swagger_auto_schema(
    method="put",
    operation_summary="Actualizar un registro",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "patient_full_name": openapi.Schema(type=openapi.TYPE_STRING),
            "patient_identifier": openapi.Schema(type=openapi.TYPE_STRING),
            "clinical_reference": openapi.Schema(type=openapi.TYPE_STRING),
            "study_date": openapi.Schema(type=openapi.TYPE_STRING, description="YYYY-MM-DD"),
        },
    ),
    responses={200: openapi.Response("Registro actualizado"), 401: openapi.Response("No autenticado"), 404: openapi.Response("No encontrado")},
)
@swagger_auto_schema(
    method="delete",
    operation_summary="Eliminar un registro",
    responses={200: openapi.Response("Registro eliminado"), 401: openapi.Response("No autenticado"), 404: openapi.Response("No encontrado")},
)
@api_view(["GET", "PUT", "DELETE"])
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


@swagger_auto_schema(
    method="get",
    operation_summary="Obtener URL firmada de imagen",
    operation_description="Genera una URL firmada con JWT que da acceso temporal (5 minutos) a la imagen del registro.",
    responses={
        200: openapi.Response("URL firmada generada"),
        401: openapi.Response("No autenticado"),
        404: openapi.Response("Registro no encontrado"),
    },
)
@api_view(["GET"])
def radiography_record_signed_image(request, record_id: int):
    db = SessionLocal()

    try:
        current_user = require_authenticated_user(request)
        record = service.get_record_detail(db, record_id)

        signed_url = generate_signed_image_url(
            request=request,
            user_id=current_user.id,
            record_id=record.id,
            image_url=record.image_url,
        )

        return JsonResponse(
            {
                "record_id": record.id,
                "signed_url": signed_url,
            },
            status=200,
        )

    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=401)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    finally:
        db.close()

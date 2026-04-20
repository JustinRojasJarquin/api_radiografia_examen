from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.api.routes.auth_routes import google_login
from core.api.routes.image_routes import view_signed_image
from core.api.routes.radiography_record_routes import (
    radiography_record_detail,
    radiography_record_list_create,
    radiography_record_signed_image,
)

schema_view = get_schema_view(
    openapi.Info(
        title="API Radiografias",
        default_version="v1",
        description="API para gestión de placas radiográficas de pacientes. "
                    "Autenticación mediante Google SSO con JWT.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/auth/google/login", google_login, name="google-login"),

    path("api/v1/records/", radiography_record_list_create, name="records-list-create"),
    path("api/v1/records/<int:record_id>/", radiography_record_detail, name="records-detail"),
    path(
        "api/v1/records/<int:record_id>/signed-image-url/",
        radiography_record_signed_image,
        name="records-signed-image-url",
    ),

    path("api/v1/images/view/", view_signed_image, name="view-signed-image"),

    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    re_path(r"^swagger\.json$", schema_view.without_ui(cache_timeout=0), name="swagger-json"),
]
from django.contrib import admin
from django.urls import path

from core.api.routes.radiography_record_routes import (
    radiography_record_detail,
    radiography_record_list_create,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/records/", radiography_record_list_create, name="records-list-create"),
    path("api/v1/records/<int:record_id>/", radiography_record_detail, name="records-detail"),
]
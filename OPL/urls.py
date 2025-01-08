from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

static_urlpatterns = [
    re_path(r"^(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Open Longevity Web API",
        default_version=settings.BUILD_VERSION,
        contact=openapi.Contact(email="openlongevitydevgroup@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/open-problems/", include("open_problems.urls")),
    path("api/posts/", include("posts_comments.urls")),
    path("api/annotations/", include("annotations.urls")),
    path("api/references/", include("references.urls")),
    path("api/users/", include("users.urls")),
    path("api/categories/", include("categories.urls")),
    path("api/static/", include(static_urlpatterns)),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/report/", include("reports.urls")),
]

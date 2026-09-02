from django.urls import include, path, re_path
from xui.ssp import views
from xui.ssp.api import viewsets

from api.routers import CloudBoltDefaultRouter

router = CloudBoltDefaultRouter()
router.register(r"api/v3/ssp/orders", viewsets.SspOrderViewSet, basename="orders")
router.register(
    r"api/v3/ssp/datatables/types",
    viewsets.SspDataTableTypeViewSet,
    basename="datatables",
)

url_path = "ssp"
xui_urlpatterns = [
    re_path(rf"^{url_path}", views.view, name="ssp"),
    path("", include(router.urls)),
]

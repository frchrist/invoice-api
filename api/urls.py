from django.urls import path, include
from rest_framework import routers



from api.views import InvoiceList, ProductViewSet, InvoiceViewSet

router = routers.DefaultRouter()

router.register("product",ProductViewSet)
router.register("invoice",InvoiceViewSet)


urlpatterns = [ 
    path("", include(router.urls)),
] 

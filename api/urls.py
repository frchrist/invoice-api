from django.urls import path, include
from rest_framework import routers



from api.views import  ProductViewSet,InvoiceAPIView, InvoiceDetailAPIView

router = routers.DefaultRouter()

router.register("product",ProductViewSet)
# router.register("invoice",InvoiceViewSet)


urlpatterns = [ 
    path("", include(router.urls)),
    path("invoice/",InvoiceAPIView.as_view(), name="invoice" ),
    path("invoice/<str:pk>/",InvoiceDetailAPIView.as_view(), name="invoice-detail" )

] 

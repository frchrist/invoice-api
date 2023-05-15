from django.urls import path, include
from rest_framework import routers



from api.views import  ProductViewSet,InvoiceAPIView, InvoiceDetailAPIView,InvoicePaginateAPIView

router = routers.DefaultRouter()

router.register("product",ProductViewSet)
# router.register("invoice",InvoiceViewSet)


urlpatterns = [ 
    path("", include(router.urls)),
    path("invoice/",InvoiceAPIView.as_view(), name="invoice" ),
    path("list_invoice/page/<int:page>/",InvoicePaginateAPIView.as_view(), name="paginate-invoice" ),

    path("invoice/<str:pk>/",InvoiceDetailAPIView.as_view(), name="invoice-detail" ),


] 

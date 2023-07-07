from django.urls import path, include
from rest_framework import routers



from api.views import  ClientDetailAPIView, ClientInvoiceAPIView,ProductViewSet,InvoiceAPIView, InvoiceDetailAPIView,InvoicePaginateAPIView, ClientAPIView

router = routers.DefaultRouter()

router.register("product",ProductViewSet)
# router.register("invoice",InvoiceViewSet)


urlpatterns = [ 
    path("", include(router.urls)),
    path("invoice/",InvoiceAPIView.as_view(), name="invoice" ),
    path("clients/",ClientAPIView.as_view(), name="client" ),
    path("clients/<str:pk>/", ClientDetailAPIView.as_view(), name="client-detail"),
    path("client_invoices/<str:pk>/",ClientInvoiceAPIView.as_view(), name="client-invoices"),
    path("list_invoice/page/<int:page>/",InvoicePaginateAPIView.as_view(), name="paginate-invoice" ),
    path("invoice/<str:pk>/",InvoiceDetailAPIView.as_view(), name="invoice-detail" ),
] 

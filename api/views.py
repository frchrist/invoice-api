from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework import Response
from rest_framework import renderers
from .process import html_to_pdf

from api.models import Invoice, Product
from api.serializers import InvoiceSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    # renderer_classes = [renderers.JSONRenderer]
    
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted= True
        instance.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class InvoiceList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset  = Invoice.objects.filter(is_deleted=False)
    serializer_class = InvoiceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, 
                        args, kwargs)

class InvoiceViewSet(viewsets.ModelViewSet):
    # renderer_classes = [renderers.JSONRenderer]
    queryset = Invoice.objects.filter(is_deleted=False)
    serializer_class = InvoiceSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted= True
        instance.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def get_queryset(self):
    #     genres = Invoice.objects.get(pk=self.kwargs.get('pk', None))
    #     movies = Movie.objects.filter(genres=genres)
    #     return movies




# Create your views here.

# class invoiceAPIView(generics.RetrieveAPIView):
#     def get(self, request, *args, **kwargs):
#         pdf =  html_to_pdf("api/invoice.html")
#         return HttpResponse(pdf, content_type="application/pdf")



# class InvoiceList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset  = Invoice.objects.all()
#     serializer_class = InvoiceSerializer

#     def post(self, request, *args, **kwargs):
#         self.serializer_class = CreateInvoiceSerializer
#         return self.create(request, args, kwargs)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, 
#                         args, kwargs)


# class ProductList(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(request, args, kwargs)
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, 
#                         args, kwargs)

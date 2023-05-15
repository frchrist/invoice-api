from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Invoice, Product
from api.serializers import InvoiceSerializer, ProductSerializer,PostInvoiceSerializer
PER_PAGES = 12
class InvoicePaginateAPIView(APIView):
    def get(self, request,page, format=None):
        try:
            start = (abs(int(page)) * PER_PAGES) - PER_PAGES
            end = abs(int(page)) * PER_PAGES
        except:
            return Http404
        invoices = Invoice.objects.filter(is_deleted=False).order_by("-created_at")[start:end]
        ser = InvoiceSerializer(invoices, many=True)

        return Response(ser.data)



class InvoiceAPIView(APIView):
    def get(self, request, format=None):
        invoices = Invoice.objects.filter(is_deleted=False).order_by("-created_at")
        ser = InvoiceSerializer(invoices, many=True)

        return Response(ser.data)

    def post(self,request,*args,**kwargs):
        ser  = PostInvoiceSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, 201)
        else:
            return Response(ser.errors, 400)

       


class InvoiceDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise 

    def get(self, request, pk, *args,**kwargs):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def delete(self, request, pk, *args,**kwargs):
        invoice = self.get_object(pk)
        invoice.is_deleted = True
        invoice.save()
        return Response({}, status.HTTP_204_NO_CONTENT)




class ProductViewSet(viewsets.ModelViewSet):
    # renderer_classes = [renderers.JSONRenderer]
    
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted= True
        instance.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)



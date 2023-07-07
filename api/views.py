from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.exceptions import InvoiceObjectNotFound
from api.models import Client, Invoice, Product
from api.serializers import ClientSerializer, InvoiceSerializer, ProductSerializer,PostInvoiceSerializer
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

class ClientAPIView(APIView):
    def get(self, request, format = None):
        clients = Client.objects.all()
        return Response(ClientSerializer(clients, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        client_serializer = ClientSerializer(data = request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response(client_serializer.data, status=status.HTTP_200_OK)
        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class ClientDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise  InvoiceObjectNotFound(message=f"{pk} client with this id not exists")

    def get(self, request, pk, *args,**kwargs):
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)



    def delete(self, request, pk, *args,**kwargs):
        client = self.get_object(pk)
        client.is_deleted = True
        client.save()
        return Response({}, status.HTTP_204_NO_CONTENT)


       


class InvoiceDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise InvoiceObjectNotFound(message=f"{pk} Invoice with this id not exists")

    def get(self, request, pk, *args,**kwargs):
        invoice = self.get_object(pk)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def delete(self, request, pk, *args,**kwargs):
        invoice = self.get_object(pk)
        invoice.is_deleted = True
        invoice.save()
        return Response({}, status.HTTP_204_NO_CONTENT)



class ClientInvoiceAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            client = Client.objects.get(id = pk)
            invoices = Invoice.objects.filter(client_field = client )
            json_parser = InvoiceSerializer(invoices, many=True)
         
            return Response(json_parser.data, status=status.HTTP_200_OK)
           
        except Exception as e:
            print(e)
            return Response({"Error" : "Invalid client ID"}, status=status.HTTP_400_BAD_REQUEST)
         




class ProductViewSet(viewsets.ModelViewSet):
    # renderer_classes = [renderers.JSONRenderer]
    
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted= True
        instance.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)



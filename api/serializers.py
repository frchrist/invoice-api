from rest_framework import serializers
from .models import Product, Invoice,ProductInInvoice, Client

class ClientSerializer(serializers.ModelSerializer):
    """
        Serializer for the client model
        @Client
    """
    invoice_type_bill_count = serializers.SerializerMethodField()
    pro_invoice_type_bill_count = serializers.SerializerMethodField()
    total_income = serializers.SerializerMethodField()
    class Meta:
        model = Client
        fields = ["id",'name', 'phone_number', "email","total_income", "pro_invoice_type_bill_count", "invoice_type_bill_count"]

    def get_pro_invoice_type_bill_count(self, obj : Client):
        return Invoice.objects.filter(client_field=obj, type="pro forma", is_deleted=False).count()
    
    def get_invoice_type_bill_count(self, obj : Client):
        return Invoice.objects.filter(client_field=obj, type="facture", is_deleted=False).count()

    def get_total_income(self, obj: Client):
        return sum([invoice.amount for invoice in Invoice.objects.filter(client_field=obj, type="facture", is_deleted=False)])
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class WriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name","unite", "price", "description")
        read_only_fields = ("price", "description","unite")


class ProductInInvoiceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price = serializers.CharField(max_length=200)
    class Meta:
        model = ProductInInvoice
        fields = "__all__"


class MySer(serializers.Serializer):
    quantity = serializers.IntegerField()
    id = serializers.CharField(max_length=200)
    price = serializers.CharField(max_length=200)





class PostInvoiceSerializer(serializers.Serializer):
    client_field =  serializers.CharField(max_length=250)
    type = serializers.CharField(max_length=100)
    product_in_invoice = MySer(many=True)
    amount = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    ref = serializers.ReadOnlyField()
    date = serializers.DateTimeField()
    created_at = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()

    def create(self, validated_data):
        products_data = validated_data.pop('product_in_invoice')
        client : str = validated_data.pop("client_field")
        client_instance : Client = Client.objects.get(id=client)
        invoice = Invoice.objects.create(**validated_data)
        invoice.client_field = client_instance
        invoice.save()
        for product_data in products_data:
            pro = Product.objects.get(id=product_data.get("id"),is_deleted=False)
            if(float(pro.price) != float(product_data.get("price"))):
                new_product_price = Product.objects.create(name=pro.name, unite=pro.unite, price = float(product_data.get("price")))
                new_product_price.save()
                pro = new_product_price

            product = ProductInInvoice.objects.create(product=pro, quantity=product_data.get("quantity"))
            invoice.product_in_invoice.add(product)
        return invoice



class InvoiceSerializer(serializers.Serializer):
    client = serializers.CharField(max_length=100)
    client_field = ClientSerializer()
    type = serializers.CharField(max_length=100)
    id = serializers.ReadOnlyField()
    product_in_invoice = ProductInInvoiceSerializer(many=True)
    amount = serializers.ReadOnlyField()
    ref = serializers.ReadOnlyField()
    date = serializers.DateTimeField()
    created_at = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()







from rest_framework import serializers
from .models import Product, Invoice,ProductInInvoice

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
    #product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field="id")
    class Meta:
        model = ProductInInvoice
        fields = "__all__"


class MySer(serializers.Serializer):
    quantity = serializers.IntegerField()
    id = serializers.CharField(max_length=200)


# class ProductSendToInvoiceSerializer(serializers.Serializer):
    # id = serializers.CharField(max_length=200)
    # # name = serializers.CharField(max_length=200)
    # quantity = serializers.IntegerField()
    # price = serializers.ReadOnlyField()
    # description = serializers.ReadOnlyField()
    # unite = serializers.ReadOnlyField()



class PostInvoiceSerializer(serializers.Serializer):
    client = serializers.CharField(max_length=100)
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
        invoice = Invoice.objects.create(**validated_data)
        for product_data in products_data:
            # pro_data = product_data.get("product")
            print(product_data)
            pro = Product.objects.get(id=product_data.get("id"),is_deleted=False)
            product = ProductInInvoice.objects.create(product=pro, quantity=product_data.get("quantity"))
            # quantity = product_data.get('quantity', 1)
            invoice.product_in_invoice.add(product)
            # InvoiceProduct.objects.create(invoice=invoice, product=product, quantity=quantity)
        return invoice



class InvoiceSerializer(serializers.Serializer):
    client = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=100)
    id = serializers.ReadOnlyField()
    product_in_invoice = ProductInInvoiceSerializer(many=True)
    amount = serializers.ReadOnlyField()
    ref = serializers.ReadOnlyField()
    date = serializers.DateTimeField()
    created_at = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()







# class InvoiceSerializer(serializers.ModelSerializer):
#     product_in_invoice = ProductSendToInvoiceSerializer(many=True)
#     # product = WriteProductSerializer(many=True)

#     amount = serializers.ReadOnlyField()
#     ref = serializers.ReadOnlyField()
#     is_deleted = serializers.ReadOnlyField()
#     # extra_kwargs = {"product" : {"write_only" : True}}



#     class Meta:
#         model = Invoice
#         fields = '__all__'
#         # read_only_fields  = ("product_in_invoice",)

#     def create(self, validated_data):
#         products_data = validated_data.pop('product_in_invoice')
#         invoice = Invoice.objects.create(**validated_data)
#         for product_data in products_data:
#             pro_data = product_data.get("product")
#             print(pro_data.get("id"))
#             pro = Product.objects.get(name=pro_data.get("name"), is_deleted=False)
#             product = ProductInInvoice.objects.create(product=pro, quantity=product_data.get("quantity"))
#             # quantity = product_data.get('quantity', 1)
#             invoice.product_in_invoice.add(product)
#             # InvoiceProduct.objects.create(invoice=invoice, product=product, quantity=quantity)
#         return invoice
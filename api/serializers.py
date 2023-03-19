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
    product = WriteProductSerializer()
    # product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field="name")
    class Meta:
        model = ProductInInvoice
        fields = "__all__"


# class ProductInvoiceSerializer(serializers.ModelSerializer):
#     quantity = serializers.IntegerField()
#     class Meta:
#         model = Product
#         fields = ("name")


class InvoiceSerializer(serializers.ModelSerializer):
    product_in_invoice = ProductInInvoiceSerializer(many=True)
    # product = WriteProductSerializer(many=True)

    amount = serializers.ReadOnlyField()
    ref = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()
    # extra_kwargs = {"product" : {"write_only" : True}}



    class Meta:
        model = Invoice
        fields = '__all__'
        # read_only_fields  = ("product_in_invoice",)

    def create(self, validated_data):
        products_data = validated_data.pop('product_in_invoice')
        invoice = Invoice.objects.create(**validated_data)
        for product_data in products_data:
            pro_data = product_data.get("product")
            pro = Product.objects.get(name=pro_data.get("name"), is_deleted=False)
            product = ProductInInvoice.objects.create(product=pro, quantity=product_data.get("quantity"))
            # quantity = product_data.get('quantity', 1)
            invoice.product_in_invoice.add(product)
            # InvoiceProduct.objects.create(invoice=invoice, product=product, quantity=quantity)
        return invoice
from django.db import models
import uuid
from datetime import date, datetime
from django.utils import timezone
from django.db.models.signals import pre_save
# Create your models here.


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name



class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    unite = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True, default="")


    def __str__(self):
        return self.name

class ProductInInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_invoice')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"




class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.CharField(max_length=25, null=True, default=None)
    client_field = models.ForeignKey(to=Client, default=None,null=True, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    ref = models.CharField(max_length=20, default="", blank=True)
   
    type = models.CharField(choices=(("pro forma", "pro forma"), ("facture", "facture")),
                            max_length=15, default="facture")
    is_deleted = models.BooleanField(default=False)
    product_in_invoice = models.ManyToManyField(to=ProductInInvoice, related_name="invoices")
    
    def __str__(self):
        return f"Facture #{self.ref}"

    @property
    def amount(self):
        return sum([int(invoice_product.product.price) * int(invoice_product.quantity) for invoice_product in self.product_in_invoice.all()])


    


def create_invoice_number(sender, instance, *args,**kwargs) -> None:
    prefix = f"KGB-"
    postfix = datetime.now().year % 100
    # FIX : int = 1000
    count = sender.objects.count() + 70
    number : str = f"{prefix}{str(count).zfill(4)}/{postfix}"
    if len(instance.ref) == 0:
        instance.ref = number



pre_save.connect(receiver=create_invoice_number, sender=Invoice)



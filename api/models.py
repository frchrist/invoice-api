from django.db import models
from datetime import date, datetime
from django.db.models.signals import pre_save
# Create your models here.




class Product(models.Model):
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # quantity = models.IntegerField(helper_text="Quantité en Stock")
    is_deleted = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True, default="")


    def __str__(self):
        return self.name

class ProductInInvoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_invoice')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"





class Invoice(models.Model):
    client = models.CharField(max_length=25, default="")
    ref = models.CharField(max_length=20, default="")
   
    type = models.CharField(choices=(("pro forma", "pro forma"), ("facture", "facture")),
                            max_length=15, default="facture")
    is_deleted = models.BooleanField(default=False)
    product_in_invoice = models.ManyToManyField(to=ProductInInvoice, related_name="invoices")
    
    def __str__(self):
        return f"Facture #{self.ref}"

    @property
    def amount(self):
        return sum([int(invoice_product.product.price) * int(invoice_product.quantity) for invoice_product in self.product_in_invoice.all()])
        # sum_ = 0
        # for invoice_product in self.article_in_invoice.all():
        #     sum_ += int(invoice_product.product.price) * int(invoice_product.quantity)



# class InvoiceProduct(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='article_in_invoice')
#     product = models.ForeignKey(ProductInInvoice, on_delete=models.CASCADE, related_name='invoice_products')
#     # quantity = models.IntegerField()

    


def create_invoice_number(sender, instance, *args,**kwargs) -> None:
    prefix = f"KG/{datetime.now().year}/"
    FIX : int = 1000
    count = sender.objects.count() + FIX
    number : str = f"{prefix}{count}"
    instance.ref = number



pre_save.connect(receiver=create_invoice_number, sender=Invoice)



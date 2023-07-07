from typing import Any, Optional
from django.core.management.base import BaseCommand
from api.models import Client, Invoice



class Command(BaseCommand):
    help  = "Utils to migrate to client model"

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.migrate()
    
    def migrate(self):
        for invoice  in Invoice.objects.all():
            invoice.client_field = self.create_or_get_client(invoice.client)
            invoice.save()
            print(invoice.id)

    def create_or_get_client(self, client_name :str):
        clt = Client.objects.filter(name = client_name).first()
        if clt == None:
            clt  = Client.objects.create(name=client_name, phone_number = "", email="no@mail.com")
        return clt
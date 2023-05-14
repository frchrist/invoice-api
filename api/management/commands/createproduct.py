from django.core.management.base import BaseCommand, CommandError
from api.models import Product, Invoice
import os
import csv

class Command(BaseCommand):
	help = "Add product from command line"

	def add_arguments(self, parser):
		pass


	def handle(self,*args,**options):
		self.read_file_content("api_product_rows.csv")
		print("[+] done")


	def read_file_content(self, filename):

		with open(f"{os.getcwd()}/{filename}") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["is_deleted"] == 'false':
					pr  = Product.objects.create(name=row.get("name"), price=row.get("price"), description=row.get("description"))
					pr.save()
					try:
						print(f"[+] {pr.pk}")
					except:
						print("Cool")
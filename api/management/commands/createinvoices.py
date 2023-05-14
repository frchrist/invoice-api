from django.core.management.base import BaseCommand, CommandError
from api.models import  Invoice
import os
import csv

class Command(BaseCommand):
	help = "Add Invoice from command line"

	def add_arguments(self, parser):
		pass


	def handle(self,*args,**options):
		self.read_file_content("api_invoice_rows.csv")
		print("[+] done")


	def read_file_content(self, filename):

		with open(f"{os.getcwd()}/{filename}") as file:
			reader = csv.DictReader(file)
			for row in reader:
				if row["is_deleted"] == 'false':
					pr  = Invoice.objects.create(client=row.get("client"),
					 date=row.get("date"),
					 ref=row.get("ref"),
					  type=row.get("type"))
					pr.save()
					try:
						print(f"[+] {pr.pk}")
					except:
						print("Cool")
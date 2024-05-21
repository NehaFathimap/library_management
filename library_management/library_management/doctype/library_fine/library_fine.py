# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryFine(Document):


	def before_submit(self):
		if frappe.db.exists("Library Transaction", self.library_transaction):
			transaction_doc = frappe.get_doc("Library Transaction",self.library_transaction)
			existing_fine = transaction_doc.fine_amount
			transaction_doc.fine_amount = existing_fine + self.fine_amount
			transaction_doc.save()

# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class LibraryMember(Document):
	#this method will run every time a document is saved
    def before_save(self):
        self.full_name = f'{self.first_name} {self.last_name or ""}'


    def autoname(self):

       format = "LM-{}-.####".format(self.first_name)
       self.name = make_autoname(format)

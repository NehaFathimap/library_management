# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class LibraryMembership(Document):
    # check before submitting this document
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                # check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")


    def validate(self):
        if self.from_date and self.to_date:
            if self.to_date < self.from_date:
                frappe.throw("<b>ToDate</b> should  not be lesser than <b>FromDate</b>")

    def autoname(self):
        format = "{}".format(self.library_member)
        self.name = make_autoname(format)

    def validate_member(self):
        return frappe.db.exists(
              "Library Membership",
                {
                    "library_member": self.library_member,
                    "docstatus": 1,
                })
    def before_save(self):
        if self.validate_member() :
            member = frappe.get_doc("Library Member",self.library_member)
            member.status = "Active"
            member.save()
        else :
            member = frappe.get_doc("Library Member",self.library_member)
            member.status = "Deactive"
            member.save()

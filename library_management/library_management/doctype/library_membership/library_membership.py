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
        # get loan period and compute to_date by adding loan_period to from_date
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)

    def validate(self):
        if self.to_date < self.from_date:
            frappe.throw("<b>ToDate</b> should  not be lesser than <b>FromDate</b>")

    def autoname(self):
        format = "{}".format(self.library_member)
        self.name = make_autoname(format)

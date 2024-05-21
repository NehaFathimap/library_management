# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document
from datetime import timedelta


class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # set the article status to be Issued
            for article in self.articles:
                article = frappe.get_doc("Article",article.article)
                article.status = "Issued"
                article.save()

        elif self.type == "Return":
            self.validate_return()
            # set the article status to be Available
            for article in self.articles:
                article = frappe.get_doc("Article", article.article)
                article.status = "Available"
                article.save()

    def validate_issue(self):
        self.validate_membership()

         # article cannot be issued if it is already issued
        for article in self.articles:
            article = frappe.get_doc("Article", article.article)
            if article.status == "Issued":
                frappe.throw("Article is already issued by another member")

    def validate_return(self):
        for article in self.articles:
            article = frappe.get_doc("Article",article.article)
        # article cannot be returned if it is not issued first
            if article.status == "Available":
                frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": 1},
        )
        if count + len(self.articles) > max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")





    def before_save(self):
         self.has_fine = self.check_fine_status()


    @frappe.whitelist()
    def check_fine_status(self):
        if self.type == "Return":
            loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
            issue_doc = frappe.db.exists('Library Transaction',{
                       "library_member": self.library_member,
                       "docstatus": 1,
                       "type": "Issue",
            })
            print("\n", issue_doc,"\n ")
            issue_date = frappe.db.get_value("Library Transaction",issue_doc,'date')
            return_date = self.date
            date_diff = frappe.utils.date_diff(return_date ,issue_date )
            print("\n", date_diff,"\n ")
            if date_diff > loan_period :
               return 1
            return 0

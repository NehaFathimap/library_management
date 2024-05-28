# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe

# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe.model.document import Document
from datetime import timedelta
from frappe.model.naming import make_autoname

class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            for article in self.articles:
                article = frappe.get_doc("Article", article.article)
                # article.number_of_copies = int(article.number_of_copies ) - 1
                if article.number_of_copies == 0:
                    article.status = "Issued"
                else:
                    article.status = "Available"
                article.save()
                self.update_issued_books(add=True)

        elif self.type == "Return":
            self.validate_return()
            for article in self.articles:
                article = frappe.get_doc("Article", article.article)
                # article.number_of_copies = int(article.number_of_copies ) + 1
                article.status = "Available"
                article.save()
            self.update_issued_books(add=False)

    def validate_issue(self):
        for row in self.get('articles'):
            article = frappe.get_doc("Article", row.article)
            if article.number_of_copies == 0:
                frappe.throw(f"No available copies of {article.name} to issue")

    def validate_return(self):
        library_member = frappe.get_doc("Library Member", self.library_member)
        article_issued = library_member.get("article_issued") or []
        for article in self.articles:
            if not any(book.article_name == article.article and not book.get('return_date') for book in article_issued):
                frappe.throw(" Article cannot be returned as without issuing first")
        for row in self.get('articles'):
            for book in article_issued:
                if book.article_name == row.article and not book.get('return_date'):
                    library_member.count = int(library_member.count) - 1
                    book.return_date = self.date
                    break
        library_member.save()

    def on_cancel(self):
        if self.type == "Issue":
            library_member = frappe.get_doc("Library Member", self.library_member)
            article_issued = library_member.get("article_issued") or []
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                article.number_of_copies = int(article.number_of_copies) + 1
                article.save()
                for book in article_issued:
                    if book.article_name == row.article and not book.get('return_date'):
                        article_issued.remove(book)
                        break
            library_member.count -= len(self.get('articles'))
            library_member.set("article_issued", article_issued)
            library_member.save()
        elif self.type == "Return":
            library_member = frappe.get_doc("Library Member", self.library_member)
            article_issued = library_member.get("article_issued") or []
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                article.number_of_copies = int(article.number_of_copies) - 1
                article.status = "Issued"
                article.save()
                for book in article_issued:
                    if book.article_name == row.article and book.get('return_date') == self.date:
                        book.return_date = None
                        break
            library_member.count = int(library_member.count) + 1
            library_member.save()

    def update_issued_books(self, add):
        library_member = frappe.get_doc("Library Member", self.library_member)
        if add:
            for row in self.get('articles'):
                article = frappe.get_doc("Article", row.article)
                if article.number_of_copies == 0:
                    frappe.throw(f"No available copies of {article.name} to issue")
                article.number_of_copies = int(article.number_of_copies) - 1
                article.save()
                library_member.append("article_issued", {
                    "article_name": article.name,
                })
        else:
            for row in self.get('articles'):
                for i, book in enumerate(library_member.get("article_issued", [])):
                    if book.article_name == row.article and not book.get('return_date'):
                        article = frappe.get_doc("Article", book.article_name)
                        article.number_of_copies = int(article.number_of_copies) + 1
                        article.save()
                        library_member.get("article_issued").pop(i)
                        break
        library_member.count = len([book for book in library_member.get("article_issued", []) if not book.get('return_date')])
        library_member.save()

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        library_member = frappe.get_doc("Library Member", self.library_member)
        article_issued = library_member.get("article_issued") or []
        count = len([book for book in article_issued  if not book.get('return_date')])
        new_issues_count = len(self.get('articles'))
        total_count = count + new_issues_count
        if total_count > max_articles:
            frappe.throw("The total count of issued articles exceeds the maximum limit")

    def validate_membership(self):
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
            issue_date = frappe.db.get_value("Library Transaction",issue_doc,'date')
            return_date = self.date
            date_diff = frappe.utils.date_diff(return_date ,issue_date )
            if date_diff > loan_period :
               return 1

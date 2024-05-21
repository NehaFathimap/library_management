# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _

def execute(filters=None):
	columns, data, report_summary =get_columns(filters), get_data(filters), get_report_summary(filters)

	message = "This is a report of articles in the Library"

	return columns, data, message, None, report_summary

def get_columns(filters):
    columns = [
        {
            'fieldname': 'name',
            'label': _('ID'),
            'fieldtype': 'Link',
            'options': 'Article',
            'width':250,
        },
        {
            'fieldname': 'article_name',
            'label': _('Article Name'),
            'fieldtype': 'Data',
			'width':100,
        },
        {
            'fieldname': 'author',
            'label': _('Author'),
            'fieldtype': 'data',
			'width':100,
        },
        {
            'fieldname': 'status',
            'label': _('Status'),
            'fieldtype': 'check',
            'options':'Issued\nAvailable',
			'width':100,
        },
        {
		'fieldname':'description',
		'label':_('Description'),
		'feildtype':'Text Editor',
		'width':250,
		},
		{
			'fieldname':'Issued_Transactions',
			'label':_("Issued Transactions"),
			'fieldtype': "Int",
			'width':100,
		},
		{
		'fieldname': 'Returned_Transaction',
		'label':_("Returned Transaction"),
		'fieldtype':"Int",
		'width':100,
		}
    ]

    return columns

def get_data(filters):
	filter = {}
	if filters.article:
		filter['name'] = filters.article
	if filters.author:
		filter['author'] = ["like", f"%{filters.author}%"]
	article_list = frappe.db.get_all("Article",filters=filter, fields=["name", "article_name", "author","status","description"])
	for article in article_list:
		article['Issued_Transactions'] = frappe.db.count("Library Transaction", filters={"article":article['name'], 'docstatus':1, 'type':"Issue"})
		article['Returned_Transaction'] = frappe.db.count("Library Transaction",filters={"article":article['name'],'docstatus':1,'type':"Return"})
	return article_list

def get_report_summary(filters):
	available_books = frappe.db.count("Article", filters={"status":"Available"})
	issued_books = frappe.db.count("Article", filters={"status":"Issued"})
	transactions_on_issue =frappe.db.count("Library Transaction",filters={"type":"Issue"})
	transactions_on_return =frappe.db.count("Library Transaction",filters={"type":"Return"})
	return [{
			"value": available_books,
			"label": _("Available Books"),
			"indicator": "Green",
			"datatype":"Data"
		},
		{
				"value": issued_books,
				"label": _("Issued Books"),
				"indicator": "Red",
				"datatype": "Data"
			},
			 {
		 			"value":transactions_on_issue,
		 			"label": _("Issued Transaction "),
		 			"indicator": "Red",
		 			"datatype": "Data"
			},
			 {
		 			"value": transactions_on_return,
		 			"label": _("Return Transaction "),
		 			"indicator": "Green",
		 			"datatype": "Data"
			}
			]

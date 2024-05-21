# Copyright (c) 2024, neha and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _

def execute(filters=None):
	columns, data =get_columns(filters), get_data(filters)
	return columns, data

def get_columns(filters):
    columns = [
        {
            'fieldname': 'name',
            'label': _('ID'),
            'fieldtype': 'Link',
            'options': 'Library Membership',
            'width':250,
        },
            {
	            'fieldname': 'library_member',
	            'label': _('Library Member'),
	            'fieldtype': 'Link',
	            'options': 'Library Member',
	            'width':250,
	        },
        {
            'fieldname': 'full_name',
            'label': _('Full Name'),
            'fieldtype': 'data',
			'width':100,
        },
        {
            'fieldname': 'from_date',
            'label': _('From Date'),
            'fieldtype': 'date',
        },
        {
            'fieldname': 'to_date',
            'label': _('to Date'),
            'fieldtype': 'date',
        }


    ]

    return columns

def get_data(filters):
	filter = {}
	if filters.full_name:
		filter['full_name'] = ["like", f"%{filters.full_name}%"]
	membership_list = frappe.db.get_all("Library Member",filters=filter, fields=["name", "Library_member","full_name" ,"from_date","to_date"])
	return membership_list

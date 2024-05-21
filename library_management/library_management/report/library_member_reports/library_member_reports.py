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
            'options': 'Library Member',
            'width':250,
        },
        {
            'fieldname': 'first_name',
            'label': _('First Name'),
            'fieldtype': 'Data',
			'width':100,
        },
        {
            'fieldname': 'full_name',
            'label': _('Full Name'),
            'fieldtype': 'data',
			'width':100,
        },
        {
            'fieldname': 'email_address',
            'label': _('Email Address'),
            'fieldtype': 'data',
        },
        {
		'fieldname':'phone',
		'label':_('Phone'),
		'feildtype':'data',
		'width':250,
		}

    ]

    return columns

def get_data(filters):
	filter = {}
	if filters.full_name:
		filter['full_name'] = ["like", f"%{filters.full_name}%"]
	member_list = frappe.db.get_all("Library Member",filters=filter, fields=["name", "first_name","last_name","full_name" ,"email_address","phone"])
	return member_list

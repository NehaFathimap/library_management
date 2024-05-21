// Copyright (c) 2024, neha and contributors
// For license information, please see license.txt

frappe.query_reports["Article Script Report"] = {
	"filters": [
		{
				fieldname: 'article',
				label: __('Article'),
				fieldtype: 'Link',
				options: 'Article'
		},
		{
				fieldname: 'author',
				label: __('Author'),
				fieldtype: 'Data',
		}
	]
};

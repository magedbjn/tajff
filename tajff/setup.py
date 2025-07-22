# import os

import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
# from frappe.desk.page.setup_wizard.install_fixtures import (
# 	_,  # NOTE: this is not the real translation function
# )
# from frappe.desk.page.setup_wizard.setup_wizard import make_records
# from frappe.installer import update_site_config


def after_install():
	create_taj_hrms_fields()

def before_uninstall():
	delete_custom_fields(get_taj_hrms_fields_fields())

def create_taj_hrms_fields():
	if "hrms" in frappe.get_installed_apps():
		create_custom_fields(get_taj_hrms_fields_fields(), ignore_validate=True)

def get_taj_hrms_fields_fields():
	return {
		"Leave Type": [
			{
				"fieldname": "taj_overlapping_days_compensated",
				"fieldtype": "Check",
				"label": _("Taj-Overlapping Days Compensated with Public Holidays"),
				"insert_after": "is_compensatory",
			},
		],
		"Leave Application": [
			{
				"fieldname": "taj_overlapping_days_compensated",
				"label": _("Overlapping Days Compensated with Public Holidays"),
				"fieldtype": "Data",
				"insert_after": "to_date",
				"read_only": 1,
			},
			{
				"fieldname": "taj_travel",
				"label": _("Travel"),
				"fieldtype": "Tab Break",
				"insert_after": "amended_from",
			},
			{
				"fieldname": "taj_travel_ticket",
				"label": _("Travel Ticket"),
				"fieldtype": "Check",
				"default": 0,
				"insert_after": "taj_travel",
			},
			{
				"fieldname": "taj_last_travel_ticket",
				"label": _("Last Travel Ticket"),
				"fieldtype": "Read Only",
				"insert_after": "taj_travel_ticket",
			},
			{
				"fieldname": "taj_status_travel_ticket",
				"label": _("Status Travel Ticket"),
				"fieldtype": "Select",
				"insert_after": "taj_last_travel_ticket",
				"options": "\nCovered by company\nReimbursable Expense\nNon-Reimbursable Expense",
				"read_only_depends_on": "eval:doc.taj_travel_ticket==0",
			},
			{
				"fieldname": "taj_column_break_mhfpk",
				"label": "",
				"fieldtype": "Column Break",
				"insert_after": "taj_status_travel_ticket",
			},
			{
				"fieldname": "taj_return_visa",
				"label": _("Return Visa"),
				"fieldtype": "Check",
				"default": 0,
				"insert_after": "taj_column_break_mhfpk",
			},
			{
				"fieldname": "taj_last_return_visa",
				"label": _("Last Return Visa"),
				"fieldtype": "Read Only",
				"insert_after": "taj_return_visa",
			},
			{
				"fieldname": "taj_status_return_visa",
				"label": _("Status Return Visa"),
				"fieldtype": "Select",
				"insert_after": "taj_last_return_visa",
				"options": "\nCovered by company\nReimbursable Expense\nNon-Reimbursable Expense",
				"read_only_depends_on": "eval:doc.taj_return_visa==0",
			}
		],
		"Gratuity": [
			{
				"fieldname": "taj_details",
				"fieldtype": "Tab Break",
				"label": _("Taj Details"),
				"insert_after": "payable_Account",
			},
			{
				"fieldname": "taj_date_of_joining",
				"fieldtype": "Date",
				"label": _("Date of Joining"),
				"read_only": 1,
				"fetch_from": "employee.date_of_joining", 
    			"fetch_if_empty": 1,  
				"insert_after": "taj_details",
			},
			{
				"fieldname": "taj_relieving_date",
				"fieldtype": "Date",
				"label": _("Relieving Date"),
				"read_only": 1,
				"fetch_from": "employee.relieving_date", 
    			"fetch_if_empty": 1,  			
				"insert_after": "taj_date_of_joining",
			},
			{
				"fieldname": "taj_column_1",
				"label": "",
				"fieldtype": "Column Break",
				"insert_after": "taj_relieving_date",
			},
			{
				"fieldname": "taj_salary",
				"label": _("Salary"),
				"fieldtype": "Currency",
				"read_only": 1,
				"insert_after": "taj_column_1",
			},
			{
				"fieldname": "taj_section_1",
				"label": "",
				"fieldtype": "Section Break",
				"insert_after": "taj_salary",
			},
			{
				"fieldname": "taj_gratuity_details",
				"fieldtype": "Table",
				"label": _("Gratuity Details"),
				"options": "Taj Gratuity Details", 
				"read_only": 1,		
				"insert_after": "taj_section_1",
			},
		],
		"BOM Operation": [
			{
				"fieldname": "taj_min_temperature",
				"fieldtype": "Float",
				"label": _("Minimum Temperature"),
				"insert_after": "image",
			},
			{
				"fieldname": "taj_max_temperature",
				"fieldtype": "Float",
				"label": _("Maximum Temperature"),
				"insert_after": "min_temperature",
			},
		],
	}

def delete_custom_fields(custom_fields: dict):
	"""
	:param custom_fields: a dict like `{'Leave Application': [{fieldname: 'Travels', ...}]}`
	"""
	for doctype, fields in custom_fields.items():
		frappe.db.delete(
			"Custom Field",
			{
				"fieldname": ("in", [field["fieldname"] for field in fields]),
				"dt": doctype,
			},
		)

		frappe.clear_cache(doctype=doctype)
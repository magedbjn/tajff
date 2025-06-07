# Copyright (c) 2025, Maged BAjandooh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_days, cint, flt, getdate

def execute(filters=None) -> tuple:
    if not filters:
        filters = {}
        
    from_date = getdate(filters.get("from_date"))
    to_date = getdate(filters.get("to_date"))
    
    if not from_date or not to_date:
        frappe.throw(_('"From Date" and "To Date" are required'))
        
    if to_date <= from_date:
        frappe.throw(_('"From Date" must be before "To Date"'))

    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "id", 
            "label": _("ID"), 
            "fieldtype": "Data", 
            "width": 150, 
            "is_tree": True
        },
        {
            "fieldname": "leave_application", 
            "label": _("Leave Application"), 
            "fieldtype": "Link", 
            "options": "Leave Application", 
            "width": 150,
            "hidden": 1
        },
        {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Data", "width": 180},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "leave_type", "label": _("Leave Type"), "fieldtype": "Link", "options": "Leave Type", "width": 150},
        {"fieldname": "from_date", "label": _("From Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "to_date", "label": _("To Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "holiday_list", "label": _("Holiday List"), "fieldtype": "Link", "options": "Holiday List", "width": 120},
        {"fieldname": "holiday_count", "label": _("Total Holidays"), "fieldtype": "Int", "width": 100},
        {"fieldname": "holiday_date", "label": _("Holiday Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "holiday_description", "label": _("Holiday Description"), "fieldtype": "Small Text", "width": 300}
    ]

def get_data(filters):
    holidays = get_holidays(filters)
    if not holidays:
        return []
        
    min_holiday = min(holidays.keys())
    max_holiday = max(holidays.keys())
    
    leave_applications = get_leave_applications(min_holiday, max_holiday)
    employee_holiday_lists = get_employee_holiday_lists([la.employee for la in leave_applications])
    
    return process_data(leave_applications, employee_holiday_lists, holidays)

def get_holidays(filters):
    holiday_data = frappe.db.sql("""
        SELECT holiday_date, description
        FROM `tabHoliday`
        WHERE weekly_off = 0
            AND holiday_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters, as_dict=1)
    
    return {h.holiday_date: h.description for h in holiday_data}

def get_leave_applications(min_date, max_date):
    return frappe.db.get_all("Leave Application",
        filters=[
            ["from_date", "<=", max_date],
            ["to_date", ">=", min_date],
            ["docstatus", "=", 1],
            ["status", "=", "Approved"]
        ],
        fields=["name", "employee", "employee_name", "from_date", "to_date", "leave_type"]
    )

def get_employee_holiday_lists(employees):
    employee_data = frappe.db.get_all("Employee",
        filters={"name": ("in", employees)},
        fields=["name", "holiday_list", "company"]
    )
    
    company_defaults = {}
    companies = {e.company for e in employee_data}
    if companies:
        comp_data = frappe.db.get_all("Company",
            filters={"name": ("in", list(companies))},
            fields=["name", "default_holiday_list"]
        )
        company_defaults = {c.name: c.default_holiday_list for c in comp_data}
    
    return {
        e.name: e.holiday_list or company_defaults.get(e.company)
        for e in employee_data
    }

def process_data(leave_applications, holiday_lists, holidays):
    data = []
    holiday_dates = set(holidays.keys())
    
    for la in leave_applications:
        holiday_list = holiday_lists.get(la.employee)
        if not holiday_list:
            continue
            
        # Calculate overlapping holidays
        overlapping_days = {
            d: holidays[d] for d in holiday_dates 
            if la.from_date <= d <= la.to_date
        }
        
        if not overlapping_days:
            continue
            
        # Create parent row for leave application
        parent_id = f"LA-{la.name}"
        parent_row = {
            "id": parent_id,
            "leave_application": la.name,
            "employee": la.employee,
            "employee_name": la.employee_name,
            "leave_type": la.leave_type,
            "from_date": la.from_date,
            "to_date": la.to_date,
            "holiday_list": holiday_list,
            "holiday_count": len(overlapping_days),
            "holiday_date": None,
            "holiday_description": None,
            "indent": 0,
            "has_children": 1,
            "parent_id": None
        }
        data.append(parent_row)
        
        # Create child rows for each holiday
        sorted_days = sorted(overlapping_days.keys())
        for idx, holiday_date in enumerate(sorted_days):
            child_id = f"{parent_id}-H{idx+1}"
            child_row = {
                "id": child_id,
                "leave_application": la.name,
                "employee": None,
                "employee_name": None,
                "leave_type": None,
                "from_date": None,
                "to_date": None,
                "holiday_list": None,
                "holiday_count": None,
                "holiday_date": holiday_date,
                "holiday_description": holidays[holiday_date],
                "indent": 1,
                "has_children": 0,
                "parent_id": parent_id
            }
            data.append(child_row)
    
    return data
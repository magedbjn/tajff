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
        {"fieldname": "id", "label": _("ID"), "fieldtype": "Link", "options": "Leave Application", "width": 150},
        {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Data", "width": 180},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "leave_type", "label": _("Leave Type"), "fieldtype": "Link", "options": "Leave Type", "width": 150},
        {"fieldname": "from_date", "label": _("From Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "to_date", "label": _("To Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "holiday_list", "label": _("Holiday List"), "fieldtype": "Link", "options": "Holiday List", "width": 120},
        {"fieldname": "holiday_count", "label": _("Total Days"), "fieldtype": "Int", "width": 80},
        {"fieldname": "holidays", "label": _("Description"), "fieldtype": "Small Text", "width": 300}
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
            
        # Prepare holiday descriptions
        sorted_days = sorted(overlapping_days.keys())
        holiday_desc = "\n".join([f"{d}: {overlapping_days[d]}" for d in sorted_days])
        
        data.append({
            "id": la.name,
            "employee": la.employee,
            "employee_name": la.employee_name,
            "leave_type": la.leave_type,
            "from_date": la.from_date,
            "to_date": la.to_date,
            "holiday_list": holiday_list,
            "holiday_count": len(overlapping_days),
            "holidays": holiday_desc
        })
    
    return data
# Copyright (c) 2025, Maged Bajandooh
# التقرير يعرض الموظفين الذين آخذوا إجازة وتعارضت إجازتهم مع الإجازات الرسمية
# الإجازات الرسمية المدخله في النظام 
# Holiday List => weekly_off= False
import frappe
from frappe import _
from frappe.utils import getdate, today

def execute(filters=None):
    filters = filters or {}
    from_date = getdate(filters.get("from_date"))
    to_date = getdate(filters.get("to_date"))

    if not from_date or not to_date:
        frappe.throw(_("Both 'From Date' and 'To Date' are required"))

    if to_date <= from_date:
        frappe.throw(_("'To Date' must be after 'From Date'"))

    columns = get_columns()
    data = get_data(filters, from_date, to_date)
    return columns, data

def get_columns():
    return [
        {"fieldname": "id", "label": _("ID"), "fieldtype": "Data", "width": 200, "hidden": 1},
        {"fieldname": "leave_application", "label": _("Leave Application"), "fieldtype": "Link", "options": "Leave Application", "width": 180},
        {"fieldname": "employee", "label": _("Employee"), "fieldtype": "Data", "width": 130},
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "leave_type", "label": _("Leave Type"), "fieldtype": "Data", "width": 120},
        {"fieldname": "from_date", "label": _("From Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "to_date", "label": _("To Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "holiday_list", "label": _("Holiday List"), "fieldtype": "Link", "options": "Holiday List", "width": 120},
        {"fieldname": "holiday_count", "label": _("Total Holidays"), "fieldtype": "Int", "width": 120},
        {"fieldname": "holiday_date", "label": _("Holiday Date"), "fieldtype": "Date", "width": 120},
        {"fieldname": "holiday_description", "label": _("Holiday Description"), "fieldtype": "Small Text", "width": 300},
        {"fieldname": "action", "label": _("Action"), "fieldtype": "HTML", "width": 120},
    ]

def get_data(filters, from_date, to_date):
    holidays = {
        h.holiday_date: h.description for h in frappe.get_all(
            "Holiday",
            filters={"weekly_off": 0, "holiday_date": ["between", [from_date, to_date]]},
            fields=["holiday_date", "description"]
        )
    }

    if not holidays:
        return []

    min_holiday = min(holidays.keys())
    max_holiday = max(holidays.keys())

    leave_applications = frappe.db.sql("""
        SELECT name, employee, employee_name, from_date, to_date, leave_type
        FROM `tabLeave Application`
        WHERE from_date <= %s AND to_date >= %s
          AND docstatus = 1 AND status = 'Approved'
          AND taj_overlapping_days_compensated IS NULL
          AND leave_type IN (
              SELECT name FROM `tabLeave Type`
              WHERE taj_overlapping_days_compensated = 1
          )
    """, (max_holiday, min_holiday), as_dict=True)

    employee_data = frappe.get_all("Employee",
        filters={"name": ["in", [la.employee for la in leave_applications]]},
        fields=["name", "holiday_list", "company"]
    )
    company_defaults = {
        c.name: c.default_holiday_list for c in frappe.get_all("Company", fields=["name", "default_holiday_list"])
    }
    holiday_lists = {
        e.name: e.holiday_list or company_defaults.get(e.company)
        for e in employee_data
    }

    data = []
    path = "tajff.tajff.report.official_holiday_within_leave_period.official_holiday_within_leave_period"
    holiday_dates = set(holidays.keys())

    for la in leave_applications:
        hl = holiday_lists.get(la.employee)
        if not hl:
            continue

        overlapping = {d: holidays[d] for d in holiday_dates if la.from_date <= d <= la.to_date}
        if not overlapping:
            continue

        parent_id = la.name
        button_html = f"""
        <button class='btn btn-xs btn-primary'
            onclick='
                const dialog = new frappe.ui.Dialog({{
                    title: __("Update Compensated Days"),
                    fields: [
                        {{
                            label: __("Number of Days"),
                            fieldname: "comp_days_input",
                            fieldtype: "Int",
                            default: {len(overlapping)},
                            reqd: 1,
                            description: __("Maximum value: {len(overlapping)}"),
                        }}
                    ],
                    primary_action_label: __("Update"),
                    secondary_action_label: __("Remove"),
                    primary_action(values) {{
                        const days = values.comp_days_input;
                        const maxDays = {len(overlapping)};
                        if (days > maxDays) {{
                            frappe.msgprint(__("Value cannot exceed maximum allowed days"));
                            return;
                        }}
                        frappe.call({{
                            method: "{path}.update_compensated_days",
                            args: {{
                                leave_application: "{la.name}",
                                days_count: days
                            }},
                            callback: r => {{
                                frappe.msgprint(r.message);
                                frappe.query_report.refresh();
                                dialog.hide();
                            }}
                        }});
                    }},
                    secondary_action() {{
                        frappe.call({{
                            method: "{path}.remove_compensated_days",
                            args: {{ leave_application: "{la.name}" }},
                            callback: r => {{
                                frappe.msgprint(r.message);
                                frappe.query_report.refresh();
                                dialog.hide();
                            }}
                        }});
                    }}
                }});
                dialog.show();
            '>{_("Update")}</button>
        """


        data.append({
            "id": parent_id,
            "leave_application": la.name,
            "employee": la.employee,
            "employee_name": la.employee_name,
            "leave_type": la.leave_type,
            "from_date": la.from_date,
            "to_date": la.to_date,
            "holiday_list": hl,
            "holiday_count": len(overlapping),
            "holiday_date": None,
            "holiday_description": None,
            "action": button_html,
            "indent": 0,
            "has_children": 1,
            "parent_id": None
        })

        for i, date in enumerate(sorted(overlapping.keys())):
            data.append({
                "id": f"{parent_id}-H{i+1}",
                "leave_application": "",
                "employee": None,
                "employee_name": None,
                "leave_type": None,
                "from_date": None,
                "to_date": None,
                "holiday_list": None,
                "holiday_count": None,
                "holiday_date": date,
                "holiday_description": overlapping[date],
                "action": "",
                "indent": 1,
                "has_children": 0,
                "parent_id": parent_id
            })

    return data

@frappe.whitelist()
def update_compensated_days(leave_application, days_count):
    days_count = float(days_count)

    # إذا كانت القيمة 0، فقط حدث الحقل واخرج
    if days_count == 0:
        frappe.db.set_value("Leave Application", leave_application, "taj_overlapping_days_compensated", 0)
        return _("Compensated days set to 0. No leave allocation was created.")

    la = frappe.get_doc("Leave Application", leave_application)

    existing_alloc = frappe.db.sql("""
        SELECT name FROM `tabLeave Allocation`
        WHERE employee = %s AND leave_type = %s
        AND from_date <= %s AND to_date >= %s
        AND docstatus = 1 LIMIT 1
    """, (la.employee, la.leave_type, la.from_date, la.to_date), as_dict=True)

    if not existing_alloc:
        frappe.throw(_("No existing Leave Allocation found for employee {0} and leave type {1}").format(
            frappe.bold(la.employee), frappe.bold(la.leave_type)
        ))

    # تحديث قيمة الحقل في الإجازة
    frappe.db.set_value("Leave Application", leave_application, "taj_overlapping_days_compensated", days_count)

    # تخصيص أيام إجازة جديدة
    allocation = frappe.get_doc("Leave Allocation", existing_alloc[0].name)
    allocation.allocate_leaves_manually(new_leaves=days_count, from_date=today())

    return _("Compensated days updated and {0} leave days manually allocated.").format(days_count)

@frappe.whitelist()
def remove_compensated_days(leave_application):
    frappe.db.set_value("Leave Application", leave_application, "taj_overlapping_days_compensated", 0)
    return _("Compensated days removed successfully.")

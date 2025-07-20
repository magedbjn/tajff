# taj_hrms/gratuity_custom.py

import frappe
from frappe import _, bold
from frappe.utils import get_datetime, getdate, get_link_to_form
from hrms.payroll.doctype.gratuity.gratuity import Gratuity
from dateutil.relativedelta import relativedelta


class Gratuity_new(Gratuity):
    # عدم خصم أيام الغياب والإجازة بدون راتب من مكافأة نهاية الخدمة
    def get_total_working_days(self) -> float:
        date_of_joining, relieving_date = frappe.db.get_value(
            "Employee", self.employee, ["date_of_joining", "relieving_date"]
        )
        if not relieving_date:
            frappe.throw(
                _("Please set Relieving Date for employee: {0}").format(
                    bold(get_link_to_form("Employee", self.employee))
                )
            )
            
        total_working_days = (get_datetime(relieving_date) - get_datetime(date_of_joining)).days
        return total_working_days


def get_employee_details(doc, method=None):
    get_salary_slip(doc)

    if not doc.taj_salary or doc.taj_salary <= 0:
        frappe.throw(_("Salary amount is missing or zero for gratuity calculation."))

    date_of_joining = doc.taj_date_of_joining
    relieving_date = doc.taj_relieving_date

    experience = calculate_experience(date_of_joining, relieving_date)
    total_years = experience["years"]

    doc.taj_gratuity_details = []  # مسح السجلات القديمة

    slabs = doc.get_gratuity_rule_slabs()
    remaining_years = total_years
    last_used_slab = slabs[-1] if slabs else None

    for slab in slabs:
        if remaining_years <= 0:
            break

        slab_length = slab.to_year - slab.from_year

        if remaining_years >= slab_length:
            doc.append("taj_gratuity_details", {
                "gratuity_rule": f"{slab.from_year} - {slab.to_year} {_('Years')}",
                "total_experience": slab_length,
                "amount": doc.taj_salary * slab.fraction_of_applicable_earnings,
                "total_amount": doc.taj_salary * slab.fraction_of_applicable_earnings * slab_length
            })
            remaining_years -= slab_length
            last_used_slab = slab
        else:
            doc.append("taj_gratuity_details", {
                "gratuity_rule": f"{slab.from_year} - {slab.to_year} {_('Years')}",
                "total_experience": remaining_years,
                "amount": doc.taj_salary * slab.fraction_of_applicable_earnings,
                "total_amount": doc.taj_salary * slab.fraction_of_applicable_earnings * remaining_years
            })
            last_used_slab = slab
            remaining_years = 0
            break

    if remaining_years > 0 and last_used_slab:
        doc.append("taj_gratuity_details", {
            "gratuity_rule": _("Extra Years Without Slab"),
            "total_experience": remaining_years,
            "amount": doc.taj_salary * last_used_slab.fraction_of_applicable_earnings,
            "total_amount": doc.taj_salary * last_used_slab.fraction_of_applicable_earnings * remaining_years
        })
    elif remaining_years > 0:
        doc.append("taj_gratuity_details", {
            "gratuity_rule": _("Can't found rules"),
            "total_experience": remaining_years,
            "amount": 0,
            "total_amount": 0
        })

    if last_used_slab:
        fraction = last_used_slab.fraction_of_applicable_earnings
        monthly_rate = doc.taj_salary * fraction / 12
        daily_rate = monthly_rate / 30

        if experience["months"] > 0:
            doc.append("taj_gratuity_details", {
                "gratuity_rule": _('Monthes'),
                "total_experience": experience["months"],
                "amount": monthly_rate,
                "total_amount": monthly_rate * experience["months"]
            })

        if experience["days"] > 0:
            doc.append("taj_gratuity_details", {
                "gratuity_rule": _('Days'),
                "total_experience": experience["days"],
                "amount": daily_rate,
                "total_amount": daily_rate * experience["days"]
            })


def calculate_experience(date_of_joining, relieving_date=None):
    start_date = getdate(date_of_joining)
    end_date = getdate(relieving_date) if relieving_date else getdate()

    if end_date < start_date:
        return {"years": 0, "months": 0, "days": 0}

    delta = relativedelta(end_date, start_date)
    return {
        "years": delta.years,
        "months": delta.months,
        "days": delta.days
    }


def get_salary_slip(doc, method=None):
    doc.taj_salary = doc.get_total_component_amount()

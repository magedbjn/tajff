import frappe
from frappe import _, bold
from frappe.utils import get_datetime, get_link_to_form
from hrms.payroll.doctype.gratuity.gratuity import Gratuity


class Gratuity_new(Gratuity):
    def get_total_working_days(self) -> float:
        # We don't want to deduct the days of Absent and LWP leave from days of end of service
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
    		
		# payroll_based_on = frappe.db.get_single_value("Payroll Settings", "payroll_based_on") or "Leave"
        # if payroll_based_on == "Leave":
		# 	total_lwp = self.get_non_working_days(relieving_date, "On Leave")
		# 	total_working_days -= total_lwp
		# elif payroll_based_on == "Attendance":
		# 	total_absent = self.get_non_working_days(relieving_date, "Absent")
		# 	total_working_days -= total_absent

		return total_working_days
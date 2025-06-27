# قبل إعتماد الرواتب ، التأكد بأن جميع الإجازات معتمدة
import frappe
from frappe import _
from hrms.payroll.doctype.payroll_entry.payroll_entry import PayrollEntry

class PayrollEntry_New(PayrollEntry):
    def on_submit(self):
        # Check for unapproved leaves before submitting
        employee_list = [e.employee for e in self.employees]
        
        if self.unapproved_leave_applications(employee_list):
            frappe.throw(_("Unapproved Leave Applications found for employees"))
        
        self.set_status(update=True, status="Submitted")
        self.create_salary_slips()

    def unapproved_leave_applications(self, employees):
        """Returns unapproved leaves for given employees in payroll period"""
        if not employees: 
            return False

        return bool(
            frappe.db.sql("""
                SELECT 1
                FROM `tabLeave Application`
                WHERE 
                    employee IN %(employees)s
                    AND docstatus = 0
                    AND status IN ('Open')
                    AND from_date <= %(end_date)s
                    AND to_date >= %(start_date)s
                LIMIT 1
            """, {
                "employees": employees,
                "end_date": self.end_date,
                "start_date": self.start_date
            })
        )

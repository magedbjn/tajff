import frappe
from frappe import _, bold
from frappe.utils import get_datetime, getdate, get_link_to_form
from hrms.payroll.doctype.gratuity.gratuity import Gratuity
from dateutil.relativedelta import relativedelta

class Gratuity_new(Gratuity):
    # عدم خصم أيام الغياب و طلب إجازة بدون راتب من نهاية الخدمة
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

		#return total_working_days



def get_employee_details(doc, method=None):
    get_salary_slip(doc)

    date_of_joining = doc.taj_date_of_joining
    relieving_date = doc.taj_relieving_date
    
    # حساب سنوات الخبرة بدقة
    experience = calculate_experience(
        date_of_joining,
        relieving_date
    )
    total_years = experience["years"]
    
    # مسح السجلات القديمة
    doc.taj_gratuity_details = []
    
    # الحصول على شرائح قاعدة المنحة
    slabs = doc.get_gratuity_rule_slabs()
    
    # توزيع سنوات الخبرة على الشرائح
    remaining_years = total_years
    last_used_slab = None
    
    for slab in slabs:
        if remaining_years <= 0:
            break
            
        slab_length = slab.to_year - slab.from_year
        
        if remaining_years >= slab_length:
            # إضافة الشريحة كاملة
            doc.append("taj_gratuity_details", {
                "gratuity_rule": f"{slab.from_year} to {slab.to_year} Years",
                "years_of_experience": slab_length,
                "amount": doc.taj_salary * slab.fraction_of_applicable_earnings,
                "total_amount": doc.taj_salary * slab.fraction_of_applicable_earnings * slab_length
            })
            remaining_years -= slab_length
            last_used_slab = slab  # تحديث آخر شريحة مستخدمة
        else:
            # إضافة جزء من الشريحة
            doc.append("taj_gratuity_details", {
                "gratuity_rule": f"{slab.from_year} to {slab.to_year} Years",
                "years_of_experience": remaining_years,
                "amount": doc.taj_salary * slab.fraction_of_applicable_earnings,
                "total_amount": doc.taj_salary * slab.fraction_of_applicable_earnings * remaining_years
            })
            last_used_slab = slab  # تحديث آخر شريحة مستخدمة
            remaining_years = 0
            break
        
    # إذا باقي سنوات والقاعدة غير متوفرة
    if remaining_years > 0:
        doc.append("taj_gratuity_details", {
                "gratuity_rule": f"Can't found Years",
                "years_of_experience": remaining_years,
                "amount": doc.taj_salary * slab.fraction_of_applicable_earnings,
                "total_amount": doc.taj_salary * slab.fraction_of_applicable_earnings * remaining_years
        })

    # حساب الشهور والأيام فقط إذا كانت هناك شريحة مستخدمة
    fraction = last_used_slab.fraction_of_applicable_earnings
    monthly_rate = doc.taj_salary * fraction / 12
    daily_rate = monthly_rate / 30
      
        # إضافة الشهور إذا كانت موجودة
    if experience["months"] > 0:
        doc.append("taj_gratuity_details", {
            "gratuity_rule": "Months",
            "years_of_experience": experience["months"],
            "amount": monthly_rate,
            "total_amount": monthly_rate * experience["months"]
        })
        
     # إضافة الأيام إذا كانت موجودة
    if experience["days"] > 0:
        doc.append("taj_gratuity_details", {
            "gratuity_rule": "Days",
            "years_of_experience": experience["days"],
            "amount": daily_rate,
            "total_amount": daily_rate * experience["days"]
        })   

def calculate_experience(date_of_joining, relieving_date=None):
    """
    حساب سنوات الخبرة بين تاريخين بدقة
    """
    from dateutil.relativedelta import relativedelta
    from frappe.utils import getdate
    
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


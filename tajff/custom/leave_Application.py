from frappe import throw, _
import frappe

def before_save(doc, method):
    if doc.custom_travel_ticket:
        set_last_approved_record(doc, "travel")
    if doc.custom_return_visa:
        set_last_approved_record(doc, "visa")

def validate_employee(doc, method):
    if doc.custom_travel_ticket and not doc.custom_status_travel_ticket:
        frappe.throw(_("Please select Travel Ticket Status."))
    
    if doc.custom_return_visa and not doc.custom_status_return_visa:
        frappe.throw(_("Please select Return Visa Status."))

def set_last_approved_record(doc, field_type):
    # Define field names and labels based on type
    check_field = "custom_travel_ticket" if field_type == "travel" else "custom_return_visa"
    status_field = "custom_status_travel_ticket" if field_type == "travel" else "custom_status_return_visa"
    reference_field = "custom_last_travel_ticket" if field_type == "travel" else "custom_last_return_visa"

    # Fetch last approved record
    last_approved = frappe.get_all("Leave Application",
        filters={
            "employee": doc.employee,
            "docstatus": 1,
            "status": "Approved",
            check_field: 1, 
            status_field: ["!=", "Non-Reimbursable Expenses"],  
            "name": ["!=", doc.name]
        },
        fields=["name", "from_date"],
        order_by="from_date desc",
        limit=1
    )

    # Set reference field value
    setattr(doc, reference_field, last_approved[0].name if last_approved else None)
    #doc.set(reference_field, last_approved)
   
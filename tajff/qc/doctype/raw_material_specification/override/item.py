import frappe
from frappe import _

def raw_material_speceification(doc, method=None):
    # Fetch the status of the Raw Material Specification for the current item
    rms_status = frappe.db.get_value(
        "Raw Material Specification", 
        {"item_code": doc.item_code}, 
        "status"
    )
    
    # Check if specification exists and is 'Rejected'
    if rms_status == 'Rejected':
        # Verify item usage flags
        if doc.is_purchase_item == 1 or doc.include_item_in_manufacturing == 1:
            # Prevent transaction with clear error message
            frappe.throw(_(
                "Item {0} cannot be used for Purchasing/Manufacturing as its "
                "Raw Material Specification is Rejected."
            ).format(frappe.bold(doc.item_code)))
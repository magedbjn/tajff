import frappe

def raw_material_speceification(doc, method=None):
    rms = frappe.db.get_value("Raw Material Specification", filters={"item_code": doc.item_code}, fieldname=["status"])
    if rms == 'Rejected' and doc.is_purchase_item == 1:
        frappe.throw('Cannot Allow Purchase. Check on Raw Material Specification.')
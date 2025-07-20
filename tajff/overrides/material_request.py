# تجميع العناصر المتشابهة و تحديث الكميات

import frappe
from frappe import _

@frappe.whitelist()
def collect_similar_items(docname):
    doc = frappe.get_doc("Material Request", docname)

    total_quantities = {}
    items_to_delete = []

    for item in doc.items:
        item_code = item.item_code
        if item_code in total_quantities:
            total_quantities[item_code] += item.qty
            items_to_delete.append(item)
        else:
            total_quantities[item_code] = item.qty

    # Remove duplicates
    for item in reversed(items_to_delete):
        doc.remove(item)

    # Update remaining items
    for item in doc.items:
        if item.item_code in total_quantities:
            item.qty = total_quantities[item.item_code]
            del total_quantities[item.item_code]

    doc.save()
    frappe.msgprint(_("Similar items were collected and quantities updated."))

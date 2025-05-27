import frappe
from frappe import _

@frappe.whitelist()
def collect_similar_items(doc):
    item_qty = {}
    items_to_delete = []

    for item in doc.items:
        item_code = item.item_code

        if item_code in item_qty:
            item_qty[item_code] = item_qty[item_code] + item_qty
            items_to_delete.append(item)
        else:
            item_qty[item_code] = item_code

    for item in items_to_delete:
        doc.items_remove(item)

    for item_code, qty in item_qty.items():
        for item in doc.items:
            if item.item_code == item_code:
                item_qty = qty
                break
# جمع ودمج العناصر المتشابهة
import frappe
from frappe import _

@frappe.whitelist()
def collect_similar_items(doc):
    # Initialize data structures
    total_quantities = {}
    items_to_delete = []

    # First pass: Collect quantities and identify duplicates
    for item in doc.items:
        item_code = item.item_code
        
        if item_code in total_quantities:
            # Accumulate quantity for duplicate items
            total_quantities[item_code] += item.qty
            # Mark duplicate item for removal
            items_to_delete.append(item)
        else:
            # Initialize for new item code
            total_quantities[item_code] = item.qty

    # Second pass: Remove duplicate items (in reverse order)
    for item in reversed(items_to_delete):
        doc.remove(item)

    # Third pass: Update quantities for remaining items
    for item in doc.items:
        if item.item_code in total_quantities:
            item.qty = total_quantities[item.item_code]
            # Remove from dict to prevent re-updating
            del total_quantities[item.item_code]
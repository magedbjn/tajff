# Copyright (c) 2024, MAged BAjandooh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class RawMaterialSpecification(Document):
    def on_submit(self):
        if self.status not in ["Approved", "Rejected"]:
            frappe.throw(_("Only 'Approved' and 'Rejected' statuses can be submitted"))
        
        self.update_item()

    def before_cancel(self):
        # Set status to Cancelled and update item
        self.status = "Cancelled"
        self.update_item()

    def update_item(self):
        update_values = {}
        message = ""
        
        if self.status == "Approved":
            update_values = {
                'is_purchase_item': 1,
                'include_item_in_manufacturing': 1
            }
        elif self.status == "Rejected":
            update_values = {
                'is_purchase_item': 0,
                'include_item_in_manufacturing': 0
            }
            message = _("Item {0} can no longer be purchased or used in production").format(
                frappe.bold(self.item_code)
            )
        else:  # Handles 'Open' and 'Cancelled' statuses
            update_values = {
                'is_purchase_item': 1,
                'include_item_in_manufacturing': 1
            }
        
        # Update item with new values
        if update_values:
            frappe.db.set_value("Item", self.item_code, update_values)
        
        # Show message only for Rejected status
        if message:
            frappe.msgprint(message, alert=True)
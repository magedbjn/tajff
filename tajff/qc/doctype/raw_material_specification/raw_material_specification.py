# Copyright (c) 2024, MAged BAjandooh and contributors
# For license information, please see license.txt

# Changes a value in an Item module :
# - Allow Purchase
# - Lead Time in days
# - Include Item In Manufacturing

import frappe
from frappe import _
from frappe.model.document import Document


class RawMaterialSpecification(Document):
	def on_submit(self):
		if self.status in ["Open", "Cancelled"]:
			frappe.throw(_("Only status 'Approved' and 'Rejected' can be submitted."))

		self.update_item()


	def before_cancel(self):
		self.status = "Cancelled"
		self.update_item()

	def update_item(self):
		message = ""
		if self.status == "Approved":
			frappe.db.set_value("Item", self.item_code, {'is_purchase_item':1, 'include_item_in_manufacturing': 1, 'custom_raw_material_specification': 'Approved'})
		elif self.status == "Rejected":
			frappe.db.set_value("Item", self.item_code, {'is_purchase_item':0, 'include_item_in_manufacturing': 0, 'custom_raw_material_specification': 'Rejected'})
			message = _("Can't be purchase or used in production. ")
			message += "<br>"
		else:
			frappe.db.set_value("Item", self.item_code, {'is_purchase_item':1, 'include_item_in_manufacturing': 1, 'custom_raw_material_specification': 'Open'})
		
		message += _("Item in stock has been modified.")
		frappe.msgprint(message)
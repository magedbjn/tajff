import frappe
from frappe import _
from frappe.model.document import Document
from erpnext.selling.doctype.party_specific_item.party_specific_item import PartySpecificItem

class PartySpecificItem_New(PartySpecificItem):
    def validate(self):
        filters = {
            "party_type": self.party_type,
            "party": self.party,
            "restrict_based_on": self.restrict_based_on,
            "based_on_value": self.based_on_value,
            "name": ("!=", self.name)
        }

        if frappe.db.exists("Party Specific Item", filters):
            frappe.throw(_("This item filter has already been applied for the {0}").format(self.party_type))
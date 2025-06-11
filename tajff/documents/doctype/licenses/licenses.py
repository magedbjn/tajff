# Copyright (c) 2025, Maged BAjandooh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, today


class Licenses(Document):
    def before_save(self):
        self.update_license_status()
    
    def update_license_status(self):
        # Core status calculation logic
        if not self.expiry_date:
            return
            
        today_date = getdate(today())
        expiry_date = getdate(self.expiry_date)
        days_difference = date_diff(expiry_date, today_date)
        
        renew_days = frappe.get_value('Licenses Type', self.license_english, 'renew') if self.license_english else 0
        
        if days_difference < 0:
            new_status = 'Expired'
        elif 0 <= days_difference <= renew_days:
            new_status = 'Renew'
        else:
            new_status = 'Active'

        if self.status != new_status:
            self.status = new_status


def scheduled_status_update():
    update_status('Licenses', filters={'status': ['!=', 'Expired']})

def update_status(doctype, filters=None):
    # Efficient batch processing with single commit
    if filters is None:
        filters = {}
    
    if 'status' not in filters:
        filters['status'] = ['!=', 'Expired']
    
    today_date = getdate(today())
    docs = frappe.get_all(doctype, filters=filters, fields=['name', 'expiry_date', 'status', 'license_english'])
    
    updates = []
    
    for doc in docs:
        if not doc.get("expiry_date"):
            continue
            
        expiry_date = getdate(doc["expiry_date"])
        days_difference = date_diff(expiry_date, today_date)
        renew_days = frappe.get_value('Licenses Type', doc.license_english, 'renew') if doc.get('license_english') else 0
        
        if days_difference < 0:
            new_status = 'Expired'
        elif 0 <= days_difference <= renew_days:
            new_status = 'Renew'
        else:
            new_status = 'Active'

        if doc.get('status') != new_status:
            updates.append({
                "name": doc["name"],
                "status": new_status
            })
    
    if updates:
        for update in updates:
            frappe.db.set_value(doctype, update["name"], "status", update["status"])
        frappe.db.commit()
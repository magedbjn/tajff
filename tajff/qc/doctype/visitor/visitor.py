# Copyright (c) 2025, Maged BAjandooh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Visitor(Document):
	def validate(self):
		existing_email = frappe.get_all('Visitor', filters={'email': self.email, 'post_date': self.post_date})
		if existing_email:
			if existing_email[0].get('name') != self.name:
				frappe.throw("This Visitor already exists for this date!")
			
	def on_submit(self):
		if self.status in ["Open"]:
			frappe.throw("Only status 'Approved' and 'Rejected' can be submitted.")
		
		self.sent_email()


	def sent_email(self):
		message = f"Dear {self.name1},<br><br>"
		message += "We hope this message finds you well.<br><br>"
		if self.status == 'Approved':
			subject = "Approval for Access to Production Area - Tajff"
			message += "You to inform you thar your request for access to production area has been approved. Please ensure that all necessary safty protocols and guidelines are followed while in the area.<br><br>"
		elif self.status == 'Rejected':
			subject = "Rejection for Access to Production Area - Tajff"
			message += "After reviewing your request for access to the production area, we regret to inform you that we are unable tp approve it at this time. <br><br>"
			message += "This decision has been made in order to ensure your well-being and to adhere to the necessary safety protocols. <br><br>"
			
		message += "If you have any questions or require further assistance, feel free to reach out. <br><br>"
		message += "Best reqards, <br><br>Team QC<br><br> Taj Food Factory For Ready Meals"
		
		recipients = [self.email]

		try:
			frappe.sendmail(
				recipients=recipients,
				subject=subject,
				message=message,
				reference_doctype=self.doctype,
				reference_name=self.name
			)
		
			# sent_email = frappe.get_all("Email Queue", filters={"reference_doctype": "Visitor", "referenece_name": self.name, "status": "Sent"})

			# if sent_email:
			# 	frappe.msgprint(f"Email sent for Visitor {self.name1}")
			# 	return True
			# else:
			# 	frappe.msgprint(f"Email Failed to send for Visitor {self.name1}")
			# 	return False
		
		except Exception as e:
			frappe.log_error(f"Error sending email for Visitor {self.name1}: {str(e)}", "Email send Error")
			return False
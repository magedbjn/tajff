// Copyright (c) 2025, Maged BAjandooh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Visitor", {
    refresh: function(frm) {
        if (frm.doc.email_status != 'Sent') {
            frappe.call({
                method: 'frappe.client.get_list',
                args:{
                    doctype: 'Email Queue',
                    filters: {
                        'reference_doctype': frm.doctype,
                        'reference_name': frm.doc.name,
                    },
                    fields: ['status'],
                    limit_page_length: 1
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        var email_queue = r.message[0].status;
                        if (email_queue === 'Sent') {
                            frm.set_value('email_status', email_queue);
                            frm.save();
                        }
                    }
                }
            });
        }
    }
});

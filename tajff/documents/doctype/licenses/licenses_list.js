frappe.listview_settings['Licenses'] = {
    "hide_name_column": true,
    "add_fields": ["attachment"],
    "buttons": [
        {
            "name": "open_attachment",
            "label": __("Open"),
            "description": __("Open Attachment"),
            "condition": function(doc) {
                // Show button only if attachment exists and is not empty
                return doc.attachment && doc.attachment.trim() !== "";
            },
            "action": function(doc) {
                if (doc.attachment && doc.attachment.trim() !== "") {
                    // Open in new tab with proper URL encoding
                    const file_url = frappe.urllib.get_full_url(
                        encodeURI(doc.attachment)
                    );
                    window.open(file_url, '_blank').focus();
                } else {
                    frappe.msgprint({
                        title: __('No Attachment'),
                        indicator: 'red',
                        message: __('No attachment found for this license')
                    });
                }
            }
        }
    ]
};
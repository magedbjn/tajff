frappe.ui.form.on('Item', {
    refresh(frm) {
        if (!frm.is_new()) {
            frappe.db.get_value('Raw Material Specification', { item_code: frm.doc.name }, 'name')
                .then(r => {
                    if (r.message && r.message.name) {
                        frm.add_custom_button(__('Raw Material Specification'), function () {
                            frappe.set_route('Form', 'Raw Material Specification', r.message.name);
                        }, __('Taj'));
                    }
                });
        }
    }
});

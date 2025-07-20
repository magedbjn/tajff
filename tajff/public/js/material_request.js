frappe.ui.form.on('Material Request', {
    refresh: function (frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__('Collect Similar Items'), function () {
                frappe.call({
                    method: 'tajff.overrides.material_request.collect_similar_items',
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function (r) {
                        if (!r.exc) {
                            frm.reload_doc();
                        }
                    }
                });
            }, __('Taj')); // هذا يضيف الزر تحت مجموعة باسم "Taj"
        }
    }
});

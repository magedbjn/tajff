frappe.ui.form.on('BOM', {
    validate(frm) {
        for (let i = 0; i < (frm.doc.operations || []).length; i++) {
            const row = frm.doc.operations[i];
            const min = row.taj_min_temperature;
            const max = row.taj_max_temperature;

            if (min !== undefined && max !== undefined) {
                if (min !== 0 && max < min) {
                    frappe.throw(__('Row {0}: Maximum Temperature must be equal to or greater than Minimum Temperature.', [row.idx]));
                }
            }
        }
    }
});
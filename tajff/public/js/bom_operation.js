frappe.ui.form.on('BOM', {
    validate(frm) {
        for (let i = 0; i < (frm.doc.operations || []).length; i++) {
            const row = frm.doc.operations[i];
            const min = row.taj_min_temperature;
            const max = row.taj_max_temperature;

            // إذا فيه max بدون min
            if ((min === undefined || min === null || min === 0) && (max !== undefined && max !== null)) {
                frappe.throw(
                    __('Row {0}: You must enter Minimum Temperature before setting Maximum Temperature.', [row.idx])
                );
            }

            // إذا min > 0 لازم max >= min
            if (min && min > 0 && max !== undefined && max !== null) {
                if (max < min) {
                    frappe.throw(
                        __('Row {0}: Maximum Temperature must be equal to or greater than Minimum Temperature.', [row.idx])
                    );
                }
            }
        }
    }
});

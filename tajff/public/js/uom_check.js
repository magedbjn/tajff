/**
 إذا وُجد صنف واحد فقط فيه uom ≠ stock_uom وconversion_factor == 1،
 يتم إظهار رسالة واضحة قابلة للترجمة،
 يتم منع الحفظ،
 ويخرج مباشرة دون إكمال التحقق لبقية البنود.
 */
(() => {
    function apply_uom_check(doctype_name) {
        frappe.ui.form.on(doctype_name, {
            before_save(frm) {
                const items = frm.doc.items || [];
                for (let i = 0; i < items.length; i++) {
                    const item = items[i];

                    const has_issue =
                        item.uom &&
                        item.stock_uom &&
                        item.uom !== item.stock_uom &&
                        parseFloat(item.conversion_factor || 0) === 1;

                    if (has_issue) {
                        const message = __(
                            "In row {0}, item <b>{1}</b> has a Unit of Measure ({2}) different from its Stock UOM ({3}), and the Conversion Factor is 1. This is likely incorrect. Please review before saving.",
                            [
                                i + 1,
                                frappe.utils.escape_html(item.item_code || __("Unknown Item")),
                                item.uom,
                                item.stock_uom
                            ]
                        );

                        frappe.throw({
                            title: __("UOM Mismatch Detected"),
                            message: message
                        });

                        return; // exit after first violation
                    }
                }
            }
        });
    }

    // List of doctypes to apply the check
    ["Purchase Order", "Purchase Receipt", "Purchase Invoice"].forEach(apply_uom_check);
})();

frappe.ui.form.on('Leave Application', {
    onload(frm) {
        set_salary_slip_query(frm);
    },
    employee(frm) {
        frm.set_value('salary_slip', null);
        set_salary_slip_query(frm);
    },
    from_date(frm) {
        frm.set_value('salary_slip', null);
        set_salary_slip_query(frm);
    },
    to_date(frm) {
        frm.set_value('salary_slip', null);
        set_salary_slip_query(frm);
    }
});

function set_salary_slip_query(frm) {
    frm.set_query('salary_slip', function() {
        // تحقق من وجود البيانات الأساسية
        if (!frm.doc.employee || !frm.doc.from_date || !frm.doc.to_date) {
            frappe.show_alert({
                message: __('Please select Employee and Leave Dates first.'),
                indicator: 'red'
            });
            return { filters: { name: null } };
        }

        return {
            filters: [
                ['employee', '=', frm.doc.employee],
                ['docstatus', '=', 1],
                ['start_date', '<=', frm.doc.to_date],
                ['end_date', '>=', frm.doc.from_date]
            ]
        };
    });
}

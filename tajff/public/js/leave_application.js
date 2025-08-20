frappe.ui.form.on('Leave Application', {
    onload: function(frm) {
        set_salary_slip_query(frm);
    },
    employee: function(frm) {
        frm.set_value('salary_slip', null);
        set_salary_slip_query(frm);
    },
    from_date: function(frm) {
        frm.set_value('salary_slip', null);
        set_salary_slip_query(frm);
    },
    to_date: function(frm) {
        frm.set_value('salary_slip', null);
        set_salary_slip_query(frm);
    }
});

function set_salary_slip_query(frm) {
    frm.set_query('salary_slip', function() {
        if (!frm.doc.employee || !frm.doc.from_date || !frm.doc.to_date) {
            frappe.msgprint(__('Please select Employee and Leave Dates first.'));
            return { filters: { name: null } };
        }

        // Optional: Check if any salary slips match before filtering
        frappe.db.count('Salary Slip', {
            employee: frm.doc.employee,
            docstatus: 1,
            start_date: ['<=', frm.doc.to_date],
            end_date: ['>=', frm.doc.from_date]
        }).then(count => {
            if (count === 0) {
                frappe.msgprint(__('No salary slips found that overlap with the leave dates.'));
            }
        });

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

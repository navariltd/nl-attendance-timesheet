frappe.ui.form.on("Payroll Entry", {
    onload: function(frm) {
        if (frm.doc.salary_slips_created && frm.doc.status !== "Queued") {
            fetch_attendance_data(frm);
        }
    },
});

function fetch_attendance_data(frm) {
    frappe.call({
        method: "nl_attendance_timesheet.controllers.add_attendance_to_salary_slip.add_attendance_data",
        args: {
            payroll_entry: frm.doc.name,
        },
    });
}
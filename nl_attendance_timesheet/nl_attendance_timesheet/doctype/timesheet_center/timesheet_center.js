// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Timesheet Center", {
    refresh: function (frm) {
        if (frm.doc.start_date && frm.doc.end_date) {
            frm.add_custom_button(__("Generate Timesheets"), function () {
                generate_timesheets(frm);
            }).addClass("btn-secondary");
        }
    },
});

function generate_timesheets(frm) {
    frappe.call({
        method: "nl_attendance_timesheet.controllers.generate_overtime_timesheets.generate_overtime_timesheets",
        args: {
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date,
        },
    });
}

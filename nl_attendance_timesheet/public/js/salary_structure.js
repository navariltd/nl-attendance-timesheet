frappe.ui.form.on("Salary Structure", {
    refresh: function (frm) {
        frm.toggle_display(
            ["salary_component", "hour_rate"],
            frm.doc.salary_slip_based_on_timesheet || frm.doc.wage_based_salary_hours
        );
        frm.toggle_reqd(
            ["salary_component", "hour_rate"],
            frm.doc.salary_slip_based_on_timesheet || frm.doc.wage_based_salary_hours
        );
        frm.toggle_reqd(
            ["payroll_frequency"],
            !frm.doc.salary_slip_based_on_timesheet || frm.doc.wage_based_salary_hours
        );
    },

    salary_slip_based_on_timesheet: function (frm) {
        frm.doc.wage_based_salary_hours = 0;
        cur_frm.refresh_field("wage_based_salary_hours");
    },

    wage_based_salary_hours: function (frm) {
        frm.doc.salary_slip_based_on_timesheet = 0;
        cur_frm.refresh_field("salary_slip_based_on_timesheet");
        frm.toggle_display(["salary_component", "hour_rate"], frm.doc.wage_based_salary_hours);
        frm.toggle_reqd(["salary_component", "hour_rate"], frm.doc.wage_based_salary_hours);
        frm.toggle_reqd("payroll_frequency", !frm.doc.wage_based_salary_hours);
        frm.toggle_display("payroll_frequency", !frm.doc.wage_based_salary_hours);
    },
});

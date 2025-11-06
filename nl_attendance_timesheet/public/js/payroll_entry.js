frappe.ui.form.on("Payroll Entry", {
  refresh: function (frm) {
    if (frm.doc.salary_slips_created && frm.doc.status !== "Queued") {
      frm.add_custom_button(
        __("Update Timesheet into Salary Slips"),
        function () {
          fetch_attendance_data(frm);
        }
      );
    }
  },
});

function fetch_attendance_data(frm) {
  frappe.call({
    method:
      "nl_attendance_timesheet.controllers.add_attendance_to_salary_slip.add_attendance_data",
    args: {
      payroll_entry: frm.doc.name,
    },
    freeze: true,
    freeze_message: __("Updating Timesheet Data..."),
    callback: function (r) {
      if (r.message) {
        frappe.show_alert({
          message: r.message,
          indicator: "green",
        });
        frm.reload_doc();
      }
    },
  });
}

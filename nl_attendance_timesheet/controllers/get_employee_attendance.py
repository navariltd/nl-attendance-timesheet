import frappe
from datetime import datetime, time
from pypika import Criterion, Order


def get_employee_attendance(employee_id, start_date, end_date):
    SETTINGS_DOCTYPE = 'Navari Custom Payroll Settings'
    include_early_entry = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'include_early_entry')

    attendance = frappe.qb.DocType('Attendance')
    employee = frappe.qb.DocType('Employee')
    shift_type = frappe.qb.DocType('Shift Type')

    conditions = [attendance.docstatus == 1, attendance.employee == employee_id, attendance.status == 'Present',
                  attendance.attendance_date[start_date:end_date]]

    query = frappe.qb.from_(attendance) \
        .inner_join(employee) \
        .on(employee.name == attendance.employee) \
        .left_join(shift_type) \
        .on(attendance.shift == shift_type.name) \
        .select(
        attendance.name.as_('name'),
        attendance.shift.as_('shift'),
        attendance.attendance_date.as_('attendance_date'),
        attendance.in_time.as_('in_time'),
        attendance.working_hours.as_('working_hours'),
        attendance.payment_hours.as_("payment_hours"),
        attendance.overtime.as_("overtime"),
        employee.holiday_list.as_('holiday_list'),
        shift_type.include_unpaid_breaks.as_('include_unpaid_breaks'),
        shift_type.unpaid_breaks_minutes.as_('unpaid_breaks_minutes'),
        shift_type.min_hours_to_include_a_break.as_('min_hours_to_include_a_break'),
        shift_type.start_time.as_('shift_start_time'),
        shift_type.end_time.as_('shift_end_time'),
    ).where(Criterion.all(conditions)).orderby(attendance.attendance_date, order=Order.asc)

    attendance_records = query.run(as_dict=True)

    """TODO: Review section, write a test"""
    if not include_early_entry:
        for entry in attendance_records:
            if entry.in_time:
                in_time_str = str(entry.in_time).split(".")[0]  # split because entry.in_time sometimes comes in this format -> 2024-02-15 08:01:48.858030
                in_time = datetime.strptime(in_time_str, '%Y-%m-%d %H:%M:%S').time()
                shift_start_time = datetime.strptime(str(entry.shift_start_time), '%H:%M:%S').time()
                shift_end_time = datetime.strptime(str(entry.shift_end_time), '%H:%M:%S').time()

                if in_time < shift_start_time:
                    extra_hours = (shift_start_time.hour - in_time.hour) + (
                                (shift_start_time.minute - in_time.minute) / 60) + (
                                              (shift_start_time.second - in_time.second) / 3600)
                    entry.working_hours -= extra_hours

                # Deduct unpaid breaks from working hours
                entry.working_hours -= entry.unpaid_breaks_minutes / 60

                # Calculate total shift hours including unpaid breaks
                total_shift_hours = (shift_end_time.hour - shift_start_time.hour) + (
                            (shift_end_time.minute - shift_start_time.minute) / 60) + (
                                                (shift_end_time.second - shift_start_time.second) / 3600) - (
                                                entry.unpaid_breaks_minutes / 60)

                if entry.working_hours > total_shift_hours:
                    entry.payment_hours = total_shift_hours
                else:
                    entry.payment_hours = entry.working_hours

    return attendance_records


def get_employee_overtime_attendance(employee, start_date, end_date):
    timesheet = frappe.qb.DocType('Timesheet')
    timesheet_detail = frappe.qb.DocType('Timesheet Detail')

    conditions = [timesheet.docstatus == 1, timesheet.employee == employee, timesheet.start_date[start_date:end_date]]

    query = frappe.qb.from_(timesheet) \
        .inner_join(timesheet_detail) \
        .on(timesheet.name == timesheet_detail.parent) \
        .select(
        timesheet_detail.activity_type.as_('activity_type'),
        timesheet.total_hours.as_('total_hours'),
        timesheet.name.as_('name'),
        timesheet.attendance.as_('attendance'),
    ).where(Criterion.all(conditions)).orderby(timesheet.start_date, order=Order.asc)

    overtime = query.run(as_dict=True)

    return overtime

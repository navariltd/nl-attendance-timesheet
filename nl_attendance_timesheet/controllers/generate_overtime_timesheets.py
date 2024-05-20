import frappe
from frappe import _
from frappe.utils.data import get_datetime, nowdate
from datetime import datetime
from pypika import Criterion

current_date = nowdate()


@frappe.whitelist()
def generate_overtime_timesheets(start_date=current_date, end_date=current_date):
    SETTINGS_DOCTYPE = 'Navari Custom Payroll Settings'
    overtime_15 = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'overtime_15_activity')
    overtime_20 = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'overtime_20_activity')

    if not overtime_15 or not overtime_20:
        frappe.throw('Please set up both Overtime 1.5 and Overtime 2.0 activities in Navari Custom Payroll Settings')

    attendance = frappe.qb.DocType("Attendance")
    employee = frappe.qb.DocType("Employee")
    shift_type = frappe.qb.DocType("Shift Type")

    conditions = [attendance.docstatus == 1, attendance.status == "Present",
                  attendance.attendance_date[start_date:end_date]]

    query = frappe.qb.from_(attendance) \
        .inner_join(employee) \
        .on(employee.name == attendance.employee) \
        .left_join(shift_type) \
        .on(attendance.shift == shift_type.name) \
        .select(
        attendance.employee.as_("employee"),
        attendance.employee_name.as_("employee_name"),
        attendance.name.as_("name"),
        attendance.shift.as_("shift"),
        attendance.attendance_date.as_("attendance_date"),
        attendance.in_time.as_("in_time"),
        attendance.out_time.as_("out_time"),
        attendance.working_hours.as_("working_hours"),
        employee.holiday_list.as_("holiday_list"),
        employee.company.as_("company"),
        employee.department.as_("department"),
        employee.holiday_list.as_("holiday_list"),
        shift_type.start_time.as_("shift_start_time"),
        shift_type.end_time.as_("shift_end_time"),
        shift_type.unpaid_breaks_minutes.as_("unpaid_breaks_minutes"),
    ).where(Criterion.all(conditions))

    attendance_records = query.run(as_dict=True)

    for entry in attendance_records:
        if entry.get('holiday_list'):
            holiday_dates = frappe.db.get_all('Holiday', filters={'parent': entry.holiday_list}, pluck='holiday_date')
            if entry.attendance_date in holiday_dates:
                total_work_duration = calculate_holiday_hours(entry)
                if total_work_duration:
                    create_new_timesheet(entry.employee, entry.employee_name, entry.company, entry.department,
                                         overtime_20, entry.in_time, entry.working_hours, entry.name)
            else:
                from_time, hours = get_from_time_and_hours(entry)
                if from_time and hours:
                    create_new_timesheet(entry.employee, entry.employee_name, entry.company, entry.department,
                                         overtime_15, from_time, hours, entry.name)
        else:
            from_time, hours = get_from_time_and_hours(entry)
            if from_time and hours:
                create_new_timesheet(entry.employee, entry.employee_name, entry.company, entry.department, overtime_15,
                                     from_time, hours, entry.name)


def calculate_holiday_hours(entry):
    if entry.out_time and entry.shift_start_time:
        in_time_dt = datetime.strptime(str(entry.in_time).split('.')[0], '%Y-%m-%d %H:%M:%S')
        out_time_dt = datetime.strptime(str(entry.out_time).split('.')[0], '%Y-%m-%d %H:%M:%S')
        shift_start_time_dt = datetime.combine(out_time_dt.date(),
                                               datetime.strptime(str(entry.shift_start_time), '%H:%M:%S').time())

        if in_time_dt < shift_start_time_dt:
            extra_hours = shift_start_time_dt.hour - in_time_dt.hour + (
                        (shift_start_time_dt.minute - in_time_dt.minute) / 60) + (
                                      (shift_start_time_dt.second - in_time_dt.second) / 3600)
            entry.working_hours -= extra_hours

        entry.working_hours -= entry.unpaid_breaks_minutes / 60

        total_work_duration = entry.working_hours
        return max(0, total_work_duration)

    return 0


def get_from_time_and_hours(entry):
    SETTINGS_DOCTYPE = 'Navari Custom Payroll Settings'
    if entry.out_time and entry.shift_end_time:
        check_out_time_str = str(entry.out_time).split(".")[0]
        check_out_time = datetime.strptime(check_out_time_str, '%Y-%m-%d %H:%M:%S').time()
        shift_end_time = datetime.strptime(str(entry.shift_end_time), '%H:%M:%S').time()
        overtime_threshold = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'overtime_threshold')

        if check_out_time > shift_end_time:
            overtime_minutes = ((check_out_time.hour - shift_end_time.hour) * 60) + (
                        check_out_time.minute - shift_end_time.minute)

            if overtime_minutes > overtime_threshold:

                """convert datetime.timedelta to datetime.time"""
                shift_end_total_seconds = entry.shift_end_time.total_seconds()
                hours = int(shift_end_total_seconds // 3600)
                minutes = int((shift_end_total_seconds % 3600) // 60)
                seconds = int(shift_end_total_seconds % 60)
                shift_end = get_datetime(f"{hours}:{minutes}:{seconds}").time()

                from_time = datetime.combine(entry.attendance_date, shift_end)

                return from_time, overtime_minutes / 60
            else:
                """Overtime is less than 30 minutes"""
                return None, None
        else:
            """Check out time is not more than shift end time"""
            return None, None
    else:
        return None, None


def create_new_timesheet(employee, employee_name, company, department, overtime_type, from_time, hours, attendance):
    timesheet = frappe.new_doc('Timesheet')
    timesheet.employee = employee
    timesheet.company = company
    timesheet.department = department
    timesheet.attendance = attendance
    timesheet.employee_name = employee_name

    timesheet.append('time_logs', {
        'activity_type': overtime_type,
        'description': overtime_type,
        'from_time': from_time,
        'hours': hours,
        'completed': 1,
    })

    timesheet.insert(ignore_permissions=True, ignore_links=True, ignore_if_duplicate=True, ignore_mandatory=True)
    frappe.db.commit()

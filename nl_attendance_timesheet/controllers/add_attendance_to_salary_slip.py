import frappe
from frappe import _
from ..controllers.get_employee_attendance import get_employee_attendance, get_employee_overtime_attendance

SETTINGS_DOCTYPE = 'Navari Custom Payroll Settings'

maximum_monthly_hours = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'maximum_monthly_hours')
overtime_15 = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'overtime_15_activity')
overtime_20 = frappe.db.get_single_value(SETTINGS_DOCTYPE, 'overtime_20_activity')

@frappe.whitelist()
def add_attendance_data(payroll_entry):
    salary_slips = frappe.db.get_all('Salary Slip', filters = { 'payroll_entry': payroll_entry, 'docstatus': 0 })

    for entry in salary_slips:
        salary_slip = frappe.get_doc('Salary Slip', entry.get('name'))
        salary_slip.attendance = []
        salary_slip.regular_overtime = []
        salary_slip.holiday_overtime = []

        salary_slip.regular_working_hours = 0
        salary_slip.overtime_hours = 0
        salary_slip.holiday_hours = 0

        attendance = get_employee_attendance(salary_slip.get('employee'), salary_slip.get('start_date'), salary_slip.get('end_date'))
        overtime_attendance = get_employee_overtime_attendance(salary_slip.get('employee'), salary_slip.get('start_date'), salary_slip.get('end_date'))
        holiday_dates = get_holiday_dates(salary_slip.get('employee'))



        if attendance:
            for attendance_entry in attendance:
                if attendance_entry.get('attendance_date') not in (holiday_dates or []) and attendance_entry.get('working_hours') > 0:
                    billiable_hours = 0

                    if not attendance_entry.get('include_unpaid_breaks'):
                        billiable_hours = attendance_entry.get('payment_hours')
                    else:
                        if attendance_entry.get('working_hours') > attendance_entry.get('min_hours_to_include_a_break'):
                            billiable_hours = attendance_entry.get('working_hours') - (attendance_entry.get('unpaid_breaks_minutes') / 60)
                        else:
                            billiable_hours = attendance_entry.get('working_hours')

                    salary_slip.append('attendance', {
                        'attendance_date': attendance_entry.get('attendance_date'),
                        'hours_worked': attendance_entry.get('working_hours'),
                        'include_unpaid_breaks': attendance_entry.get('include_unpaid_breaks'),
                        'unpaid_breaks_minutes': attendance_entry.get('unpaid_breaks_minutes'),
                        'min_hours_to_include_a_break': attendance_entry.get('min_hours_to_include_a_break'),
                        'billiable_hours': billiable_hours
                    })

                    salary_slip.regular_working_hours += billiable_hours

        if overtime_attendance:
            for overtime_attendance_record in overtime_attendance:
                if overtime_attendance_record.get('activity_type') == overtime_15:
                    salary_slip.append('regular_overtime', {
                        'timesheet': overtime_attendance_record.get('name'),
                        'hours': overtime_attendance_record.get('total_hours')
                    })
                    salary_slip.overtime_hours += overtime_attendance_record.get('total_hours')

                if overtime_attendance_record.get('activity_type') == overtime_20:
                    salary_slip.append('holiday_overtime', {
                        'timesheet': overtime_attendance_record.get('name'),
                        'hours': overtime_attendance_record.get('total_hours')
                    })
                    salary_slip.holiday_hours += overtime_attendance_record.get('total_hours')

        if salary_slip.regular_working_hours > maximum_monthly_hours:
            salary_slip.overtime_hours += salary_slip.regular_working_hours - maximum_monthly_hours
            salary_slip.regular_working_hours = maximum_monthly_hours
        elif salary_slip.regular_working_hours < maximum_monthly_hours:
            balance_to_maximum_monthly_hours = maximum_monthly_hours - salary_slip.regular_working_hours
            if salary_slip.overtime_hours <= balance_to_maximum_monthly_hours:
                salary_slip.regular_working_hours += salary_slip.overtime_hours
                salary_slip.overtime_hours = 0
            else:
                salary_slip.overtime_hours -= balance_to_maximum_monthly_hours
                salary_slip.regular_working_hours += balance_to_maximum_monthly_hours



        if salary_slip.attendance or salary_slip.regular_overtime or salary_slip.holiday_overtime:
            salary_slip.save(ignore_permissions=True)
            frappe.db.commit()

def get_holiday_dates(employee):
    holiday_list = frappe.db.get_value('Employee', employee, 'holiday_list')
    if holiday_list:
        dates = frappe.db.get_all('Holiday', filters = { 'parent': holiday_list }, pluck = 'holiday_date')
        return dates
    return None
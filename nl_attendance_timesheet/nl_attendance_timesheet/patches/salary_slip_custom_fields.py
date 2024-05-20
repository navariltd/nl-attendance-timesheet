import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():

    custom_fields = {
        "Salary Slip": [
            {
                "fieldname": "wage_based_salary_hours",
                "fieldtype": "Check",
                "label": "Wage based salary (hours)",
                "translatable": 1,
                "read_only": 1,
                "fetch_from": "salary_structure.wage_based_salary_hours",
                "insert_after": "salary_slip_based_on_timesheet"
            },
            {
                "fieldname": "attendance_details_tab_break",
                "fieldtype": "Tab Break",
                "label": "Attendance Details",
                "translatable": 1,
                "depends_on": "eval:doc.wage_based_salary_hours",
                "insert_after": "deduct_tax_for_unsubmitted_tax_exemption_proof"
            },
            {
                "fieldname": "attendance_section",
                "fieldtype": "Section Break",
                "insert_after": "attendance_details_tab_break",
                "label": "Attendance",
                "collapsible": 1
            },
            {
                "fieldname": "attendance",
                "fieldtype": "Table",
                "options": "VF Attendance",
                "label": "Attendance",
                "translatable": 1,
                "insert_after": "attendance_section"
            },
            {
                "fieldname": "overtime_section",
                "fieldtype": "Section Break",
                "insert_after": "attendance",
                "label": "Overtime Details",
                "collapsible": 1
            },
            {
                "fieldname": "regular_overtime",
                "fieldtype": "Table",
                "options": "Regular Overtime",
                "label": "Overtime 1.5",
                "translatable": 1,
                "insert_after": "overtime_section"
            },
            {
                "fieldname": "navari_vf_cb_ss_02",
                "fieldtype": "Column Break",
                "insert_after": "regular_overtime"
            },
            {
                "fieldname": "holiday_overtime",
                "fieldtype": "Table",
                "options": "Holiday Overtime",
                "label": "Overtime 2.0",
                "translatable": 1,
                "insert_after": "navari_vf_cb_ss_02"
            },
            {
                "fieldname": "worked_hours_summary_section",
                "fieldtype": "Section Break",
                "insert_after": "holiday_overtime",
                "label": "Worked Hours Summary",
                "collapsible": 1
            },
            {
                "fieldname": "regular_working_hours",
                "fieldtype": "Float",
                "label": "Regular Working Hours",
                "translatable": 1,
                "read_only": 1,
                "insert_after": "worked_hours_summary_section"
            },
            {
                "fieldname": "overtime_hours",
                "fieldtype": "Float",
                "label": "Overtime Hours",
                "translatable": 1,
                "read_only": 1,
                "insert_after": "regular_working_hours"
            },
            {
                "fieldname": "holiday_hours",
                "fieldtype": "Float",
                "label": "Holiday Hours",
                "translatable": 1,
                "read_only": 1, 
                "insert_after": "overtime_hours"
            },
            {
                "fieldname": "navari_vf_cb_ss_01",
                "fieldtype": "Column Break",
                "insert_after": "holiday_hours"
            },
            {
                "fieldname": "hourly_rate",
                "fieldtype": "Currency",
                "label": "Hourly Rate",
                "translatable": 1,
                "fetch_from": "salary_structure.hour_rate",
                "insert_after": "navari_vf_cb_ss_01"
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)
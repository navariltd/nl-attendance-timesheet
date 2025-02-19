import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():

    custom_fields = {
        "Salary Structure": [
            {
                "fieldname": "wage_based_salary_hours",
                "fieldtype": "Check",
                "label": "Wage based salary (hours)",
                "translatable": 1,
                "insert_after": "salary_slip_based_on_timesheet",
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)

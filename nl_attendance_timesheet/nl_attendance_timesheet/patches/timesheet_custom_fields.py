import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Timesheet": [
            {
                "fieldname": "attendance",
                "fieldtype": "Link",
                "options": "Attendance",
                "label": "Attendance",
                "translatable": 1,
                "hidden": 1,
                "read_only": 1,
                "unique": 1,
                "insert_after": "note"
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)
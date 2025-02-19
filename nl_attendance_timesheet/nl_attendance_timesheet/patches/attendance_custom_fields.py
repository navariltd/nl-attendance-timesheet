import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    custom_fields = {
        "Attendance": [
            {
                "fieldname": "overtime",
                "fieldtype": "Float",
                "translatable": 1,
                "read_only": 1,
                "insert_after": "payment_hours",
            },
        ]
    }

    create_custom_fields(custom_fields, update=True)

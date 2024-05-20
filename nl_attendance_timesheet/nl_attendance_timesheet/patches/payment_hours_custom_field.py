import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Attendance": [
            {
                "fieldname": "payment_hours",
                "fieldtype": "Float",
                "label": "Payment Hours",
                "translatable": 1,
                "read_only": 1,
                "insert_after": "working_hours"
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)
import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    custom_fields = {
        "Navari Custom Payroll Settings": [
         {
                "fieldname": "overtime_threshold",
                "fieldtype": "Float",
                "label": "Overtime Threshold",
                "insert_after": "include_early_entry",
                "default": "30.0"
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)

    singles_entry = frappe.get_doc({
        "doctype": "Navari Custom Payroll Settings",
        "doctype_or_field": "Singles",
        "fieldname": "overtime_threshold",
        "value": "30.0"
    })
    singles_entry.insert()


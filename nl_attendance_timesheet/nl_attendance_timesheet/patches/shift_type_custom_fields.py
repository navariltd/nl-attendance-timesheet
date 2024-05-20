import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():

    custom_fields = {
        "Shift Type": [
            {
                "fieldname": "include_unpaid_breaks",
                "fieldtype": "Check",
                "label": "Include Unpaid Breaks",
                "translatable": 1,
                "insert_after": "end_time"
            },
            {
                "fieldname": "unpaid_breaks_minutes",
                "fieldtype": "Float",
                "label": "Unpaid breaks (minutes)",
                "translatable": 1,
                "depends_on": "eval: doc.include_unpaid_breaks",
                "insert_after": "include_unpaid_breaks"
            },
            {
                "fieldname": "min_hours_to_include_a_break",
                "fieldtype": "Float",
                "label": "Min. hours to include a break",
                "translatable": 1,
                "depends_on": "eval: doc.include_unpaid_breaks",
                "insert_after": "unpaid_breaks_minutes"
            }
        ]
    }

    create_custom_fields(custom_fields, update=True)
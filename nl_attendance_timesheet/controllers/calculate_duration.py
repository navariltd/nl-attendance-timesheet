import frappe
from frappe.utils import date_diff

def calculate_duration(doc, method):
    if doc.completion_date and doc.start_date:
        doc.duration = date_diff(doc.completion_date, doc.start_date)
    else:
        doc.duration = 0
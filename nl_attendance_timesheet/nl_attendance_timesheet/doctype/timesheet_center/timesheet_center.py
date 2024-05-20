# Copyright (c) 2024, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TimesheetCenter(Document):
	def validate(self):
		if self.start_date > self.end_date:
			frappe.throw('Start date cannot be greater than end date')

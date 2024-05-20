# Copyright (c) 2024, Navari Limited and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from csf_ke.csf_ke.doctype.timesheet_center.timesheet_center import TimesheetCenter


class TestTimesheetCenter(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_doc = TimesheetCenter(
            doctype="Timesheet Center",
            start_date="2024-01-01",
            end_date="2024-01-31"
        )

    @classmethod
    def tearDownClass(cls):
        cls.test_doc.delete()

    def test_validate_start_date_before_end_date(self):
        timesheet_center = self.test_doc
        timesheet_center.validate()

        self.assertTrue(True)

    def test_validate_start_date_after_end_date(self):
        timesheet_center = TimesheetCenter(
            doctype="Timesheet Center",
            start_date="2024-01-31",
            end_date="2024-01-01"
        )

        with self.assertRaises(frappe.ValidationError):
            timesheet_center.validate()

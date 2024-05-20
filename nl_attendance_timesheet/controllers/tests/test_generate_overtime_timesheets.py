from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from csf_ke.controllers.generate_overtime_timesheets import generate_overtime_timesheets


class TestGenerateOvertimeTimesheets(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        frappe.delete_doc("Timesheet")

    @patch('navari_vf.controllers.generate_overtime_timesheets.frappe.db.get_single_value')
    def test_generate_overtime_timesheets_no_activities_set(self, mock_get_single_value):
        mock_get_single_value.return_value = None
        with self.assertRaises(Exception):
            generate_overtime_timesheets()

    def test_generate_overtime_timesheets_with_activities_set(self):
        generate_overtime_timesheets()


    def test_generate_overtime_timesheets_no_attendance_records(self):
        generate_overtime_timesheets()


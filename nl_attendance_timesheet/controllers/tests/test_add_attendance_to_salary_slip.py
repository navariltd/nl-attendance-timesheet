from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from csf_ke.controllers.add_attendance_to_salary_slip import get_holiday_dates

class TestAddAttendanceToSalarySlip(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        frappe.delete_doc("Timesheet")

    def test_get_holiday_dates_with_employee_holiday_list(self):
        employee = 'EMPLOYEE_ID_WITH_HOLIDAY_LIST'

        expected_dates = ['2024-01-01', '2024-02-14', '2024-05-01']

        with patch('frappe.get_all', return_value=expected_dates):
            dates = get_holiday_dates(employee)

        self.assertEqual(dates, expected_dates)

    def test_get_holiday_dates_without_employee_holiday_list(self):
        employee = 'EMPLOYEE_ID_WITHOUT_HOLIDAY_LIST'

        with patch('frappe.get_all', return_value=None):
            dates = get_holiday_dates(employee)

        self.assertIsNone(dates)

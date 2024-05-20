import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import now_datetime
from csf_ke.controllers.get_employee_attendance import get_employee_attendance


class TestGetEmployeeAttendance(FrappeTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.insert_test_data()

    @classmethod
    def insert_test_data(cls):
        employee = frappe.get_doc({
            "doctype": "Employee",
            "employee_name": "Tonny Oluoch Owuor",
            "first_name": "Tonny",
            "last_name": "Owuor",
            "gender": "Male",
            "date_of_birth": "1997-10-20",
            "date_of_joining": "2021-10-15",
            "department": "Hatchery - VFL",
            "employment_type": "Contract",
        })
        employee.insert()

        shift_type = frappe.get_doc({
            "doctype": "Shift Type",
            "name": "FARM ADMINISTRATIONS SHIFT",
            "short_name": "Farm Adm",
        })
        shift_type.insert()

        # Create test Attendance records
        attendance_date = now_datetime().date()
        if not frappe.db.exists("Attendance", {"employee": employee.name, "attendance_date": attendance_date}):
            attendance = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee.name,
                "status": "Present",
                "attendance_date": attendance_date,
                "in_time": now_datetime().replace(hour=7, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S"),
                "working_hours": 9,
                "shift": shift_type.name,
            })
            attendance.insert()

    def test_get_employee_attendance(self):
        employee_id = "Test Employee ID"
        start_date = now_datetime().replace(day=1).date()
        end_date = now_datetime().date()

        attendance_records = get_employee_attendance(employee_id, start_date, end_date)

        self.assertIsNotNone(attendance_records)

        expected_attendance_count = 0
        self.assertEqual(len(attendance_records), expected_attendance_count)

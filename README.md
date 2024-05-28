# Attendance and Timesheet Integration
Frappe App to calculate and create timesheets from attendance records

## Introduction

This app includes functionalities to calculate and create timesheets from attendance records. The timesheets are created based on any hours above normal working hours, recorded in attendance.

---
## Key Features

### Doctypes
1. Employee Checkin
2. Attendance
3. Activity Type
4. Timesheet Center
5. Timesheet
6. Navari Custom Payroll Settings
7. Timesheet Center
    - Overtime Generation Process
    - Activity Types
8. Navari Custom Payroll Settings
   - [Matching Attendance to Payroll](#matching-attendance-to-payroll)
       - [Steps](#steps)
   - [Payroll Generation](#payroll-generation)
     - [Steps for Payroll Generation](#steps-for-payroll-generation)

## Doctypes

### Employee Checkin

Each employee should have an Attendance ID mapped to the biometric/RFID devices' user IDs. Devices send check-in/out logs to the Employee Checkin doctype. 

There's a need for Checkin/Checkout logs, mostly fetched from a biometric system (e.g. https://github.com/navariltd/navari-frappehr-biostar) created under [employee checkin](https://frappehr.com/docs/v14/en/employee_checkin), every day.


### Attendance

Tracks the attendance status of employees (Present, Absent, On Leave, etc.) based on Employee Checkin records.
Attendance is marked as per the shifts assigned to each employee. This happens automatically for every shift type with *Enable Auto Attendance* checked.
Overtime timesheets are generated, from the attendance data. Happens automatically, one can also choose to generate these manually from the [timesheet center.](#Timesheet_Center)


### Activity Type

Defines the different types of activities i.e.
- **Overtime 1.5**: Additional time (more than 30 minutes) past an employee's shift end time.
- **Overtime 2.0**: Attendance on a holiday listed for the employee.

**NB:** *Overtime 1.5 Activity* and *Overtime 2.0 Activity* should be different so as to differentiate between the two types of overtime.

### Timesheet Center

Serves as a hub for managing overtime generation from employee attendance records.
### Overtime Generation Process

To generate the overtime timesheets:
1. Select the start and end dates for which you want to generate timesheets.
2. Save the document.
3. Click on the **Generate Timesheets** button, which will then get employees who have worked extra hours. This will be recorded under the Timesheet doctype.


### Timesheet

Records the details of overtime hours worked by employees.

### Navari Custom Payroll Settings
This doctype includes settings related to payroll:
- **Maximum monthly hours**: Hours beyond this are carried over to overtime when creating salary slips.
- **Overtime 1.5 Activity**: Specifies the activity type for regular overtime.
- **Overtime 2.0 Activity**: Specifies the activity type for holiday overtime.
- **Include early entry**: Determines whether hours before shift start time are included in payroll calculations.
- **Overtime Threshold**: The number of minutes/hours after shift end time for overtime to be considered.

## Matching Attendance to Payroll

### Steps

1. **Create an [Employee](https://frappehr.com/docs/v14/en/employee)**: Ensure each employee is properly set up in the system.
2. **Create [Salary Components](https://frappehr.com/docs/v14/en/salary-component)**: Define the various salary components such as basic salary, allowances, and deductions.
3. **Create a [Salary Structure](https://frappehr.com/docs/v14/en/salary-structure)**: Develop a salary structure that includes all salary components.
4. **Create a [Salary Structure Assignment](https://frappehr.com/docs/v14/en/salary-structure-assignment)**: Assign the salary structure to each employee.
5. **Create a [Payroll Entry](https://frappehr.com/docs/v14/en/payroll-entry)**: Generate payroll entries for each payroll period.
6. **Generate [Salary Slips](https://frappehr.com/docs/v14/en/salary-slip)**: Create salary slips for each employee, incorporating attendance and overtime data.

## Payroll Generation

### Steps for Payroll Generation

1. **Attendance Data**: Ensure that attendance data is accurately logged and verified in the [Attendance](https://frappehr.com/docs/v14/en/attendance) doctype.
2. **Generate Overtime Timesheets**: Automatically or manually generate timesheets for overtime using the Timesheet Center for the specified payroll period.
![Timesheet Center](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/908523fc-7961-4064-916d-55e65adbd649)
3. **Submit Timesheets**: Submit timesheets to ensure they are included in payroll calculations.
![Submitted Timesheet](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/72ddcc6d-e028-4b4b-b5d3-d65131c574b4)
4. **Create Payroll Entry**: Create a payroll entry for the desired payroll period.
![Payroll Entry](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/8feb26ea-d3f3-426b-bd12-075a27dc2625)
5. **Generate Salary Slips**: Generate salary slips, which will incorporate attendance and timesheet records under the attendance tab in the salary slip, ensuring accurate calculation of regular and overtime pay.

***Few changes to the payroll process:***
1. When creating a salary structure for employees who are paid per hour, make sure to check the *Wage based salary (hours)* field, and fill the *Hour Rate* and *Salary Component* fields.
2. When running payroll on payroll entry, after generating salary slips, attendance data is fetched and added to employees attendance in the salary slips. Attendance data will be picked from [attendance](https://frappehr.com/docs/v14/en/attendance) and timesheet records generated over that payroll period.
![Attendance Details Tab](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/885be677-0406-4496-8691-894a97cb5f3d)

3. Attendance data will be added to the *Attendance Details* tab on a salary slip.
![Worked Hours Summary Section](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/80c468ba-4b44-48a4-ac6d-63deaf5fae86)

4. **Regular Working Hours:** Sum of *Billiable Hours* from the *Attendance* table. Hours beyond what is set as *Maximum monthly hours* on *Navari Custom Payroll Settings* are carried over to the *Overtime Hours* field.<br>
5. **Overtime Hours:** Sum of hours from *Overtime 1.5* table plus what has been carried over from *Regular Working Hours*, incase there is anything to carry over.<br>
6. **Holiday hours:** Sum of hours from *Overtime 2.0* table.<br>
7. **Hourly Rate:** Fetched from the salary structure assigned to an employee. Used to calculate basic and overtime pay (Both regular and holiday overtime)<br>
```Basic salary = (hourly_rate * regular_working_hours)``` <br>
```OT hours = hourly_rate * 1.5 * overtime_hours``` <br>
```Holiday Hours = hourly_rate * 2 * holiday_hours```<br>
*NB: OT here refers to regular overtime*<br>

    
## Installation
### Manual Installation
1. [Install bench](https://github.com/frappe/bench)
2. [Install ERPNext](https://github.com/frappe/erpnext#installation)
3. [Install Frappe HR](https://github.com/frappe/hrms)
4. Once bench, ERPNext and Frappe HR are installed, add nl_attendance_timesheet to your bench by running
    ```sh
        $ bench get-app https://github.com/navariltd/nl-attendance-timesheet.git
    ```
    Replace <i>{branch-name}</i> with any of the repository's branches
5. After that, you can install the nl_attendance_timesheet app on the required site by running 
    ```sh
        $ bench --site {sitename} install-app nl_attendance_timesheet
    ```
    Replace <i>{sitename}</i> with the name of your site

### Frappe Cloud Installation
### Adding the App to Your Bench

1. **Log Into Frappe Cloud Dashboard:**
   - Access your account on Frappe Cloud and navigate to the dashboard.

2. **Navigate to your Bench Apps Section:**
   - In the bench, locate and click on the **Apps** tab. This section allows you to manage all apps available to your bench.

3. **Add New App:**
   - Click on the **Add App** button. You will be prompted to enter details about the app you wish to add.
   - For **App URL**, input `https://github.com/navariltd/nl-attendance-timesheet`. Note: Since this is a private repository, you might be asked to provide credentials to access the repository.

4. **Complete the Addition:**
   - Follow any additional prompts to complete the app addition process. This might include specifying branch names if you're not using the default branch.

### Installing the App on a Specific Site

After adding the app to your bench, the next step is to install it onto the specific site where you want it to be available.

1. **Access Your Sites:**
   - From the Frappe Cloud dashboard, navigate to the **Sites** section where you'll see a list of your ERPNext sites.

2. **Select Your Site:**
   - Click on the site you wish to install the app on.

3. **Install the App:**
   - Go to the Apps tab of the site and click the **Install App** button. Selecting this option will present you with a list of apps available to install.
   - Find `Nl Attendance Timesheet` in the list and proceed with the installation.

### Verification and Use

- **Verify the Installation:**
  - Once the installation process completes, verify that the app is correctly installed by accessing your ERPNext site and checking the list of installed apps.

- **Use the App:**
  - Explore the functionalities added by `nl-attendance-timesheet` to ensure everything works as expected.

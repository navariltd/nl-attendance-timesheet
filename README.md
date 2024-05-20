# Attendance <-> Timesheet
Frappe App to calculate and create timesheets from attendance records

## Introduction

This app includes functionalities to calculate and create timesheets from attendance records. The timeseets are created based on any hours above normal working hours, recorded in attendance.

---
## Creating Timesheets from Employee Attendance

**Overtime is marked in two scenarios:**
1. Additional time (more than 30 minutes in an attendance record) past an employee's shift end time. (Overtime 1.5)
2. An attendance created on a day that is also on an employee's holiday list. (overtime 2.0)

***Timesheet Center***
Even though the overtime timesheets are created automatically, there may be scenarios where we would want to do this manually. Hence the ***Timesheet Center*** doctype.<br> 
![Screenshot from 2024-05-17 14-56-26](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/9f41ec51-06ba-4f5f-a800-93bec9961f9a)
Select the *Start Date* and *End Date* for which you want to generate the overtime timesheets.<br>
Save the document.<br>
Click on the *Generate Timesheets* button.<br>
**NB:** Timesheet Center is a [Single Doctype](https://frappeframework.com/docs/user/en/basics/doctypes/single-doctype)

### 4. Payroll
<a id="Payroll"></a>
The doctype below, *Navari Custom Payroll Settings* is important while linking attendance data to payroll. <br>

##### Navari Custom Payroll Settings
---
<a id="Navari_Custom_Payroll_Settings"></a>
As the name suggests, settings related to payroll are stored here.

![Screenshot from 2024-05-17 15-12-44](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/4e473d4f-c225-429e-bc14-fa36dbc75ed5)

1. *Maximum monthly hours:* The maximum number of hours beyond which, the rest is carried over to overtime while creating employee salary slips.
2. *Overtime 1.5 Activity:* Overtime 1.5 is what the employee gets for working past their shift time, on a regular day. We tag the activity set here while creating timesheets for overtime 1.5
3. *Overtime 2.0 Activity:* Overtime 2.0 is what the employeee gets for working on a day that appears on their holiday list. We tag the activity set here while creating timesheets for overtime 2.0
4. *Include early entry:* When checked, hours before shift start time will be considered while making employee salary slips. When uncheked, working hours will be calculated from the shift start time while making salary slips, doesn't matter if an employee checked in earlier for their shift.

**NB:** *Overtime 1.5 Activity* and *Overtime 2.0 Activity* should be different so as to differentiate between the two types of overtime.

## How attendance is matched to payroll
<a id="how_attendance_is_matched_to_payroll"></a>
This is how payroll works on ERPNext:
1. Create an [employee.](https://frappehr.com/docs/v14/en/employee)
2. Create [salary components.](https://frappehr.com/docs/v14/en/salary-component)
3. Create a [salary structure.](https://frappehr.com/docs/v14/en/salary-structure)
4. Create a [salary structure assignment](https://frappehr.com/docs/v14/en/salary-structure-assignment) for each employee.
5. Create a [payroll entry](https://frappehr.com/docs/v14/en/payroll-entry) and generate [salary slips](https://frappehr.com/docs/v14/en/salary-slip) for each employee.

### Steps for Payroll Generation
With Attendance based payroll, there are a few more steps while generating salary slips for employees who are paid per hour.
1. There's a need for Checkin/Checkout logs, mostly fetched from a biometric system (e.g. https://github.com/navariltd/navari-frappehr-biostar) created under [employee checkin](https://frappehr.com/docs/v14/en/employee_checkin), after every hour.
2. Attendance is marked as per the shifts assigned to each employee. This happens automatically for every shift type with *Enable Auto Attendance* checked.
![Screenshot from 2024-05-17 15-18-48](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/87badc65-79f3-4f12-9810-5991858f7d01)
3. Overtime timesheets are generated, from the attendance data. Happens automatically, one can also choose to generate these manually from the [timesheet center.](#Timesheet_Center)
![Screenshot from 2024-05-17 15-19-19](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/8bf63740-7111-4d69-a9ba-031806dd3f5b)
4. Timesheets need to be submitted for them to be considered when running payroll.

***Few changes to the payroll process:***
1. When creating a salary structure for employees who are paid per hour, make sure to check the *Wage based salary (hours)* field, and fill the *Hour Rate* and *Salary Component* fields.
![Screenshot from 2024-05-17 22-27-21](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/b09aeeae-ecf9-4542-a2f5-e8c99cd2cbff)
2. When running payroll on payroll entry, after generating salary slips, attendance data is fetched and added to employees attendance in the salary slips. Attendance data will be picked from [attendance](https://frappehr.com/docs/v14/en/attendance) and timesheet records generated over that payroll period.
3. Attendance data will be added to the *Attendance Details* tab on a salary slip.
![Screenshot from 2024-05-17 22-31-11](https://github.com/navariltd/nl-attendance-timesheet/assets/60260520/44c3fd26-c789-4aac-871b-376db5051f16)

<br>
*1. Attendance:* Picked from an employee's attendance records over that payroll period<br>
> *Payment Hours* - this is a custom field in attendance doctype which accurately captures total shift hours, excluding unpaid breaks if any and overtime. It is captured as billable hours in Attendance Details in Salary Slip.<br>

*2. Overtime 1.5:* Picked from timesheet records, timesheets with the activity type set as *Overtime 1.5 Activity* on *VF Payroll Settings*<br>
*3. Overtime 2.0:* Picked from timesheet records, timesheets with the activity type set as *Overtime 2.0 Activity* on *VF Payroll Settings*<br>
*4. Regular Working Hours:* Sum of *Billiable Hours* from the *Attendance* table. Hours beyond what is set as *Maximum monthly hours* on *VF Payroll Settings* are carried over to the *Overtime Hours* field.<br>
*5. Overtime Hours:* Sum of hours from *Overtime 1.5* table plus what has been carried over from *Regular Working Hours*, incase there is anything to carry over.<br>
*6. Holiday hours:* Sum of hours from *Overtime 2.0* table.<br>
*7. Hourly Rate:* Fetched from the salary structure assigned to an employee. Used to calculate basic and overtime pay (Both regular and holiday overtime)<br>
See salary structure below:
![Screenshot from 2024-05-17 22-34-31](https://github.com/navariltd/navari_csf_ke/assets/60260520/fcc6c265-efb6-425e-9c26-ddb0a348c55b)

```Basic salary = (hourly_rate * regular_working_hours)``` <br>
```OT hours = hourly_rate * 1.5 * overtime_hours``` <br>
```Holiday Hours = hourly_rate * 2 * holiday_hours```<br>
*NB: OT here refers to regular overtime*<br>
See how the hours from the above screenshots reflect on earnings and deductions:
![Screenshot from 2024-05-17 22-49-36](https://github.com/navariltd/navari_csf_ke/assets/60260520/1d0c770f-de32-451c-b1e8-704330bfe398)

    
## Installation
### Manual Installation
1. [Install bench](https://github.com/frappe/bench)
2. [Install ERPNext](https://github.com/frappe/erpnext#installation)
3. [Install Frappe HR](https://github.com/frappe/hrms)
4. Once bench, ERPNext and Frappe HR are installed, add navari_vf to your bench by running
    ```sh
        $ bench get-app --branch {branch-name} git@github.com:navariltd/nl-attendance-timesheet.git
    ```
    Replace <i>{branch-name}</i> with any of the repository's branches
5. After that, you can install the navari_vf app on the required site by running 
    ```sh
        $ bench --site {sitename} install-app nl-attendance-timesheet
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
   - Find `Navari VF` in the list and proceed with the installation.

### Verification and Use

- **Verify the Installation:**
  - Once the installation process completes, verify that the app is correctly installed by accessing your ERPNext site and checking the list of installed apps.

- **Use the App:**
  - Explore the functionalities added by `nl-attendance-timesheet` to ensure everything works as expected.

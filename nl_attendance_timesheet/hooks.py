app_name = "nl_attendance_timesheet"
app_title = "FrappeHR Attendance and Timesheet Integration"
app_publisher = "Navari Ltd"
app_description = "FrappeHR dependent app to create employee timesheets from attendance records"
app_email = "support@navari.co.ke"
app_license = "GNU Affero General Public License v3.0"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/nl_attendance_timesheet/css/nl_attendance_timesheet.css"
# app_include_js = "/assets/nl_attendance_timesheet/js/nl_attendance_timesheet.js"

# include js, css files in header of web template
# web_include_css = "/assets/nl_attendance_timesheet/css/nl_attendance_timesheet.css"
# web_include_js = "/assets/nl_attendance_timesheet/js/nl_attendance_timesheet.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "nl_attendance_timesheet/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "nl_attendance_timesheet.utils.jinja_methods",
# 	"filters": "nl_attendance_timesheet.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "nl_attendance_timesheet.install.before_install"
# after_install = "nl_attendance_timesheet.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "nl_attendance_timesheet.uninstall.before_uninstall"
# after_uninstall = "nl_attendance_timesheet.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "nl_attendance_timesheet.utils.before_app_install"
# after_app_install = "nl_attendance_timesheet.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "nl_attendance_timesheet.utils.before_app_uninstall"
# after_app_uninstall = "nl_attendance_timesheet.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "nl_attendance_timesheet.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"nl_attendance_timesheet.tasks.all"
# 	],
# 	"daily": [
# 		"nl_attendance_timesheet.tasks.daily"
# 	],
# 	"hourly": [
# 		"nl_attendance_timesheet.tasks.hourly"
# 	],
# 	"weekly": [
# 		"nl_attendance_timesheet.tasks.weekly"
# 	],
# 	"monthly": [
# 		"nl_attendance_timesheet.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "nl_attendance_timesheet.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "nl_attendance_timesheet.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "nl_attendance_timesheet.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["nl_attendance_timesheet.utils.before_request"]
# after_request = ["nl_attendance_timesheet.utils.after_request"]

# Job Events
# ----------
# before_job = ["nl_attendance_timesheet.utils.before_job"]
# after_job = ["nl_attendance_timesheet.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"nl_attendance_timesheet.auth.validate"
# ]

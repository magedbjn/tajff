app_name = "tajff"
app_title = "Taj Food Factory"
app_publisher = "Maged BAjandooh"
app_description = "Taj Food Factory for Ready Meals"
app_email = "m.bajandooh@tajff.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "tajff",
# 		"logo": "/assets/tajff/logo.png",
# 		"title": "Taj Food Factory",
# 		"route": "/tajff",
# 		"has_permission": "tajff.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tajff/css/tajff.css"
# app_include_js = "/assets/tajff/js/tajff.js"

# include js, css files in header of web template
# web_include_css = "/assets/tajff/css/tajff.css"
# web_include_js = "/assets/tajff/js/tajff.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tajff/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tajff/public/icons.svg"

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
# 	"methods": "tajff.utils.jinja_methods",
# 	"filters": "tajff.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tajff.install.before_install"
# after_install = "tajff.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tajff.uninstall.before_uninstall"
# after_uninstall = "tajff.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "tajff.utils.before_app_install"
# after_app_install = "tajff.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tajff.utils.before_app_uninstall"
# after_app_uninstall = "tajff.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tajff.notifications.get_notification_config"

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

doc_events = {
    "Item":{
        'before_save': "tajff.qc.doctype.raw_material_specification.override.item.raw_material_speceification"
    },
    "Leave Application": {
        "before_save": "tajff.custom.leave_Application.before_save",
        "before_submit": "tajff.custom.leave_Application.validate_employee"
	},
    # "Licenses":{
    #     'before_save': "tajff.documents.doctype.licenses.licenses.before_save",
    #     'on_update': "tajff.documents.doctype.licenses.licenses.on_update"
    # },
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
 }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"tajff.documents.doctype.licenses.licenses.scheduled_status_update"
	],
	# "daily": [
	# 	"tajff.tasks.daily"
	# ],
	# "hourly": [
	# 	"tajff.tasks.hourly"
	# ],
	# "weekly": [
	# 	"tajff.tasks.weekly"
	# ],
	# "monthly": [
	# 	"tajff.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "tajff.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tajff.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tajff.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tajff.utils.before_request"]
# after_request = ["tajff.utils.after_request"]

# Job Events
# ----------
# before_job = ["tajff.utils.before_job"]
# after_job = ["tajff.utils.after_job"]

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
# 	"tajff.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"doctype": "Client Script",},
    {"doctype": "Server Script",},
    #{"doctype": "Custom Field",},
    {"doctype": "Custom Field","filters": [
        [
            "dt", "in", [
                "Leave Application"
			]
		]
	]},
    # {"doctype": "Item", "filters": 
    #  [["custom_raw_material_specification", "in", [
    #     "Rejected","Approved"
    # ]]]},
#    {"doctype": "Custom Field", "filters": [["name", "in", [
#        "Item-custom_raw_material_specification",
#        "Item-item_name_arabic",
#    ]]]},
]

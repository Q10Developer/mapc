# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ProjectProgressUpdate(Document):
	def validate(self):
		self.validate_project_scope()

	def validate_project_scope(self):
		if self.project and self.developer:
			project_developer = frappe.db.get_value("Civil Project", self.project, "developer")
			if project_developer and project_developer != self.developer:
				frappe.throw(
					_("Developer {0} does not own project {1}.").format(self.developer, self.project),
					frappe.ValidationError,
				)

		if self.location and self.project:
			location_project = frappe.db.get_value("Project Location", self.location, "project")
			if location_project and location_project != self.project:
				frappe.throw(
					_("Location {0} does not belong to project {1}.").format(self.location, self.project),
					frappe.ValidationError,
				)

		if self.project_activity:
			activity = frappe.db.get_value(
				"Project Activity",
				self.project_activity,
				["project", "location"],
				as_dict=True,
			)
			if activity:
				if self.project and activity.project != self.project:
					frappe.throw(
						_("Project Activity {0} does not belong to project {1}.").format(
							self.project_activity, self.project
						),
						frappe.ValidationError,
					)
				if self.location and activity.location != self.location:
					frappe.throw(
						_("Project Activity {0} is not assigned to location {1}.").format(
							self.project_activity, self.location
						),
						frappe.ValidationError,
					)

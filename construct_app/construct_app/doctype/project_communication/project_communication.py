# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ProjectCommunication(Document):
	def validate(self):
		if self.location and self.project:
			location_project = frappe.db.get_value("Project Location", self.location, "project")
			if location_project and location_project != self.project:
				frappe.throw(
					_("Location {0} does not belong to project {1}.").format(self.location, self.project),
					frappe.ValidationError,
				)

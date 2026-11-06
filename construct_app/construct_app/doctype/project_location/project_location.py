# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class ProjectLocation(NestedSet):
	nsm_parent_field = "parent_project_location"

	def validate(self):
		if self.project and self.location_code:
			duplicate = frappe.db.exists(
				"Project Location",
				{
					"project": self.project,
					"location_code": self.location_code,
					"name": ["!=", self.name],
				},
			)
			if duplicate:
				frappe.throw(
					_("Location Code {0} is already used in this project.").format(self.location_code),
					frappe.ValidationError,
				)


def on_doctype_update():
	frappe.db.add_unique("Project Location", ["project", "location_code"])

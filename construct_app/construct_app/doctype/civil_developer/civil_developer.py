# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _
from frappe.model.document import Document


class CivilDeveloper(Document):
	def validate(self):
		if not re.fullmatch(r"[A-Z0-9]{3,12}", self.developer_code or ""):
			frappe.throw(
				_("Developer Code must contain 3 to 12 uppercase letters or digits."),
				frappe.ValidationError,
			)

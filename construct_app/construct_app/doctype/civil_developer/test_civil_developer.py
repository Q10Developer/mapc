# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestCivilDeveloper(IntegrationTestCase):
	def test_valid_developer_code(self):
		developer = frappe.new_doc("Civil Developer")
		developer.developer_name = "Example Developer"
		developer.developer_code = "DEV123"

		developer.validate()

	def test_developer_code_must_be_uppercase_and_3_to_12_characters(self):
		for code in ("ab1", "AB", "ABCDEFGHIJKLM", "AB-1"):
			with self.subTest(code=code), self.assertRaises(frappe.ValidationError):
				developer = frappe.new_doc("Civil Developer")
				developer.developer_name = "Example Developer"
				developer.developer_code = code
				developer.validate()

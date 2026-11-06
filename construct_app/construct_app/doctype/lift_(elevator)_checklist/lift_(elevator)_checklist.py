# Copyright (c) 2026, Astha and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class LiftElevatorChecklist(Document):
	pass


globals()["Lift(Elevator)Checklist"] = LiftElevatorChecklist

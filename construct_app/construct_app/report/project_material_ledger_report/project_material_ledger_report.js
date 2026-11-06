frappe.query_reports["Project Material Ledger Report"] = {
	filters: [
		{
			fieldname: "project",
			label: __("Project"),
			fieldtype: "Link",
			options: "Civil Project",
			reqd: 1,
		},
		{
			fieldname: "party_type",
			label: __("Party Type"),
			fieldtype: "Select",
			options: "\nSupplier\nContractor",
			reqd: 1,
		},
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier",
			depends_on: "eval:doc.party_type == 'Supplier'",
			reqd: 1,
		},
		{
			fieldname: "contractor",
			label: __("Contractor"),
			fieldtype: "Link",
			options: "Project Party",
			depends_on: "eval:doc.party_type == 'Contractor'",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
		},
	],
};

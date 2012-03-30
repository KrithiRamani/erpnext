# ERPNext - web based ERP (http://erpnext.com)
# Copyright (C) 2012 Web Notes Technologies Pvt Ltd
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
	This patch removes wrong indexs and add proper indexes in tables
"""

import webnotes
sql = webnotes.conn.sql
from webnotes.utils import cint, cstr

def create_proper_index():
	from webnotes.modules.export_module import export_to_files

	dt_index_fields={
						'Purchase Receipt Item': ['prevdoc_docname', 'item_code', 'warehouse', 'prevdoc_detail_docname'], 
						'Period Closing Voucher': ['closing_account_head', 'fiscal_year'], 
						'Lead': ['lead_name', 'status', 'transaction_date'], 
						'Time Sheet Detail': ['app_name'], 
						'Item Quality Inspection Parameter': [], 
						'Budget Detail': ['fiscal_year', 'account'], 
						'Grade': [], 
						'Sales Taxes and Charges': ['parenttype', 'account_head'], 
						'TDS Category Account': ['account_head'], 
						'Role': [], 
						'Leave Allocation': ['leave_type', 'employee', 'fiscal_year'], 
						'Branch': [], 
						'Department': [], 
						'Contact Detail': [], 
						'Territory': ['lft', 'rgt', 'parent_territory'], 
						'Item Tax': ['tax_type'], 
						'Bin': ['warehouse', 'item_code'], 
						'PPW Detail': ['warehouse'], 
						'Sales Partner': ['partner_name'], 
						'Default Home Page': ['home_page', 'role'], 
						'Custom Field': ['dt'], 
						'DocFormat': ['format'], 
						'DocType Mapper': ['from_doctype', 'to_doctype'], 
						'Brand': [], 
						'Quotation Lost Reason': [], 
						'Journal Voucher': ['posting_date', 'voucher_type'], 
						'TDS Return Acknowledgement': ['date_of_receipt', 'acknowledgement'], 
						'BOM Report Detail': ['item_code'], 
						'Quotation Item': ['item_code'], 
						'Update Delivery Date Detail': ['sales_order_no'], 
						'Sales Invoice Advance': ['journal_voucher'], 
						'Authorization Rule': ['approving_user', 'system_user', 'system_role', 'approving_role'], 
						'DocPerm': ['permlevel', 'role'], 
						'Stock Entry Detail': ['item_code', 't_warehouse', 's_warehouse'], 
						'Stock Entry': ['posting_date', 'delivery_note_no', 'purchase_receipt_no', 'production_order'], 
						'Price List': [], 
						'Appraisal Template Goal': [], 
						'Production Order': ['status', 'project_name', 'production_item'], 
						'Account': ['lft', 'rgt', 'parent_account'], 
						'Earn Deduction Detail': [], 
						'Purchase Request': ['status', 'transaction_date'], 
						'Tag Detail': [], 
						'Salary Slip Deduction': ['d_type'], 
						'Batch': ['item'], 
						'Deduction Type': [], 
						'Project': ['project_name', 'customer'], 
						'UserRole': ['role'], 
						'DocField': ['label', 'fieldtype', 'fieldname'], 
						'Property Setter': ['doc_type', 'doc_name', 'property'], 
						'Appraisal': ['status', 'employee'], 
						'Letter Head': [], 
						'Communication Log': ['follow_up_by'], 
						'Project Cost Breakup': [], 
						'Table Mapper Detail': [], 
						'Campaign': [], 
						'SMS Parameter': [], 
						'Leave Type': [], 
						'Account Balance': ['period', 'start_date', 'end_date', 'account'], 
						'Absent Days Detail': [], 
						'Tag': [], 
						'Raw Materials Supplied': ['raw_material'], 
						'Project Activity Update': [], 
						'Purchase Receipt Item Supplied': [], 
						'Bank Reconciliation Detail': ['voucher_id'], 
						'Sales Order': ['quotation_no', 'project_name', 'customer', 'posting_date'], 
						'Chapter VI A Detail': [], 
						'Employee Internal Work History': [], 
						'Order Reconciliation Detail': ['sales_order_no'], 
						'Attendance': ['employee', 'att_date'], 
						'Employee External Work History': [], 
						'Salary Structure Earning': ['e_type'], 
						'Sales Order Item': ['item_code', 'prevdoc_docname', 'reserved_warehouse'], 
						'Appraisal Template': [], 
						'Budget Distribution': ['fiscal_year'], 
						'Workstation': ['warehouse'], 
						'Period': [], 
						'Training Session Details': [], 
						'Sales Taxes and Charges Master': [], 
						'State': [], 
						'Bulk Rename Tool': [], 
						'Landed Cost Master Detail': [], 
						'Employee': ['employee_name', 'designation', 'department'], 
						'Terms And Conditions': [], 
						'TC Detail': [], 
						'UOM': [], 
						'Supplier Type': [], 
						'Project Milestone': [], 
						'Landed Cost Master': [], 
						'Budget Distribution Detail': [], 
						'Form 16A Ack Detail': [], 
						'Campaign Expense': [], 
						'Time Sheet': ['employee_name', 'time_sheet_date'], 
						'File Group': ['parent_group'], 
						'Maintenance Visit Purpose': ['item_code', 'service_person'], 
						'Support Ticket Response': [], 
						'Purchase Invoice Item': ['item_code', 'purchase_order', 'po_detail', 'purchase_receipt', 'pr_detail', 'expense_head', 'cost_center'], 
						'Timesheet Detail': ['project_name', 'task_id', 'customer_name'], 
						'Holiday': [], 
						'Workflow Rule Detail': [], 
						'Module Def': ['module_seq', 'module_page'], 
						'Terms and Conditions': [], 
						'PF Detail': ['item_code'], 
						'POS Setting': ['user', 'territory'], 
						'Quality Inspection Reading': [], 
						'Support Ticket': ['customer', 'allocated_to', 'status'], 
						'Project Activity': ['project'], 
						'Customer Group': ['lft', 'rgt', 'parent_customer_group'], 
						'Sales and Purchase Return Item': ['item_code'], 
						'Series Detail': [], 
						'Event Role': ['role'], 
						'Contact': ['employee_id'], 
						'BOM Item': ['item_code', 'bom_no'], 
						'Invest 80 Declaration Detail': [], 
						'Purchase Order Item Supplied': [], 
						'Industry Type': [], 
						'Declaration Detail': [], 
						'Holiday List': ['fiscal_year'], 
						'Sales Person': ['lft', 'rgt', 'parent_sales_person'], 
						'Sales Invoice Item': ['item_code', 'sales_order', 'so_detail', 'delivery_note', 'dn_detail', 'cost_center', 'income_account'], 
						'Module Def Item': [], 
						'TDS Category': [], 
						'DocTrigger': [], 
						'Print Format': ['standard'], 
						'Installation Note Item': ['prevdoc_docname', 'item_code'], 
						'Form 16A Tax Detail': [], 
						'Event': ['event_date', 'event_type'], 
						'Currency': [], 
						'Service Quotation Detail': ['item_code'], 
						'Warehouse Type': ['warehouse_type'], 
						'Sales BOM': ['item_group'], 
						'IT Checklist': ['employee'], 
						'Purchase Taxes and Charges Master': [], 
						'Company': [], 
						'Call Log': [], 
						'Employee Training': [], 
						'Warehouse': ['warehouse_type'], 
						'Competitor': [], 
						'Mode of Payment': [], 
						'Training Session': ['customer'], 
						'Cost Center': ['lft', 'rgt', 'parent_cost_center'], 
						'Timesheet': ['status', 'timesheet_date'], 
						'Form 16A': ['party_no'], 
						'Sales BOM Item': ['item_code'], 
						'Answer': ['question'], 
						'Supplier': [], 
						'Installation Note': ['delivery_note_no', 'customer', 'inst_date'], 
						'Expense Claim': ['approval_status', 'employee'], 
						'Target Detail': ['from_date', 'to_date', 'fiscal_year'], 
						'Page Role': ['role'], 
						'Partner Target Detail': ['fiscal_year', 'item_group'], 
						'Shipping Address': ['customer'], 
						'Purchase Request Item': ['item_code', 'warehouse'], 
						'TDS Payment Detail': [], 
						'Market Segment': [], 
						'Comment': [], 
						'Service Order Detail': ['item_code', 'prevdoc_docname'], 
						'TDS Payment': ['from_date', 'to_date', 'tds_category'], 
						'Lead Email CC Detail': [], 
						'User Setting-Role User': [], 
						'Salary Slip': ['month', 'year', 'employee'], 
						'Maintenance Schedule Detail': ['item_code', 'scheduled_date'], 
						'Employment Type': [], 
						'Purchase Invoice Advance': ['journal_voucher'], 
						'Quotation': ['customer', 'transaction_date'], 
						'Salary Structure Deduction': ['d_type'], 
						'BOM': ['item', 'project_name'], 
						'Earning Type': [], 
						'Designation': [], 
						'BOM Replace Utility Detail': ['parent_bom'], 
						'Question': [], 
						'Stock Ledger Entry': ['item_code', 'warehouse', 'posting_date', 'posting_time'], 
						'Employee Education': [], 
						'BOM Operation': [], 
						'Item Group': ['lft', 'rgt', 'parent_item_group'], 
						'Workflow Action Detail': [], 
						'User Setting-Profile': [], 
						'Customer Issue': ['item_code', 'customer', 'complaint_date'], 
						'Feed': [], 
						'Purchase Taxes and Charges': ['account_head'], 
						'GL Mapper Detail': [], 
						'TDS Detail': [], 
						'PRO Detail': ['item_code', 'source_warehouse'], 
						'DocType Label': [], 
						'Sales Invoice': ['posting_date', 'debit_to', 'project_name'], 
						'GL Entry': ['posting_date', 'account', 'voucher_no'], 
						'Serial No': ['status', 'warehouse'], 
						'Delivery Note': ['posting_date', 'project_name', 'customer'], 
						'UOM Conversion Detail': ['uom'], 
						'Search Criteria': ['criteria_name'], 
						'Salary Structure': [], 
						'Educational Qualifications': ['qualification'], 
						'TDS Rate Chart': ['applicable_from', 'applicable_to'], 
						'GL Mapper': [], 
						'Announcement': [], 
						'Call Log Details': [], 
						'Opportunity': ['lead', 'customer', 'transaction_date'], 
						'BOM Explosion Item': ['item_code'], 
						'Landed Cost Item': ['account_head'], 
						'Field Mapper Detail': ['from_field', 'to_field'], 
						'File Data': [], 
						'Question Tag': [], 
						'Quality Inspection': ['item_code', 'purchase_receipt_no', 'report_date'], 
						'Appraisal Goal': [], 
						'POS Settings': ['territory'], 
						'Delivery Note Item': ['item_code', 'prevdoc_docname', 'warehouse', 'prevdoc_detail_docname'], 
						'Profile': [], 
						'Other Income Detail': [], 
						'Product': ['item_code', 'stock_warehouse'], 
						'Purchase Order Item': ['prevdoc_docname', 'item_code', 'prevdoc_detail_docname', 'warehouse'], 
						'Module Def Role': ['role'], 
						'Sales Team': ['sales_person'], 
						'Opportunity Item': ['item_code'], 
						'DocType': [], 
						'Compaint Note': ['nature_of_complaint', 'compliance_date'], 
						'Maintenance Schedule': ['customer', 'sales_order_no'], 
						'Event User': ['person'], 
						'Stock Reconciliation': ['reconciliation_date'], 
						'Purchase Receipt': ['posting_date', 'supplier', 'project_name'], 
						'Complaint Detail': ['item_name'], 
						'Address': ['customer', 'supplier'], 
						'Task': ['request_date', 'allocated_to', 'category', 'customer', 'project'], 
						'Territory Target Detail': ['month', 'fiscal_year'], 
						'Landed Cost Purchase Receipt': ['purchase_receipt_no'], 
						'Customer': ['customer_name', 'customer_group'], 
						'Production Plan Sales Order': [], 
						'Production Plan Item': ['document_date', 'item_code', 'parent_item'], 
						'User Setting-Role Permission': [], 
						'Custom Script': ['dt'], 
						'Country': [], 
						'DefaultValue': [], 
						'Multi Ledger Report Detail': [], 
						'Salary Slip Earning': ['e_type'], 
						'SMS Log': [], 
						'Expense Claim Type': [], 
						'Item': ['item_group'], 
						'Fiscal Year': [], 
						'ToDo': ['role'], 
						'Purchase Invoice': ['posting_date', 'credit_to', 'project_name', 'supplier'], 
						'Journal Voucher Detail': ['account', 'against_voucher', 'against_invoice', 'against_jv'], 
						'Online Contact': [], 
						'Page': ['module'], 
						'Leave Application': ['employee', 'leave_type', 'from_date', 'to_date'], 
						'Expense Claim Detail': ['expense_type'], 
						'Maintenance Visit': ['customer', 'sales_order_no', 'customer_issue_no'], 
						'Item Price': ['price_list_name', 'ref_currency'], 
						'SMS Receiver': [], 
						'Naming Series Options': ['doc_type'], 
						'Activity Type': [], 
						'PRO Production Plan Item': [], 
						'Delivery Note Packing Item': ['item_code', 'parent_item', 'warehouse'], 
						'Workflow Rule': ['select_form'], 
						'File': ['file_group'], 
						'Maintenance Schedule Item': ['item_code', 'start_date', 'end_date', 'prevdoc_docname'], 
						'Purchase Order': ['supplier', 'project_name', 'posting_date'], 
						'Print Heading': [], 
						'TDS Rate Detail': ['category']
					}
	#sql("commit") # only required if run from login
	exist_dt = [cstr(d[0]) for d in sql("select name from `tabDocType`")]
	
	for dt in [d for d in dt_index_fields.keys() if d in exist_dt]:
		try:
			current_index = sql("show indexes from `tab%s`" % dt)
	
			proper_index = dt_index_fields[dt]
	
			for d in current_index:
				if d[4] not in ['name', 'parent', 'parenttype']:
					if d[4] not in proper_index:
						sql("ALTER TABLE `tab%s` DROP INDEX %s" % (dt, d[4]))
						sql("start transaction")
						sql("UPDATE `tabDocField` SET search_index = 0 WHERE fieldname = '%s' AND parent = '%s'" % (d[4], dt))
						sql("commit")
					else:
						proper_index.remove(d[4])
	
			for d in proper_index:
				sql("ALTER TABLE `tab%s` ADD INDEX ( `%s` ) " % (dt, d))
				sql("start transaction")
				sql("UPDATE `tabDocField` SET search_index = 1 WHERE fieldname = '%s' AND parent = '%s'" % (d, dt))
				sql("commit")
		except:
			continue
			
def execute():
	create_proper_index()	

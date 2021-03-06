from __future__ import unicode_literals
import frappe
import random
from frappe.utils import random_string, add_days, cint
from erpnext.projects.doctype.timesheet.test_timesheet import make_timesheet
from erpnext.projects.doctype.timesheet.timesheet import make_salary_slip, make_sales_invoice
from frappe.utils.make_random import get_random
from erpnext.hr.doctype.expense_claim.expense_claim import get_expense_approver, make_bank_entry
from erpnext.hr.doctype.leave_application.leave_application import get_leave_balance_on, OverlapError

def work():
	frappe.set_user(frappe.db.get_global('demo_hr_user'))
	year, month = frappe.flags.current_date.strftime("%Y-%m").split("-")
	prev_month = str(cint(month)- 1).zfill(2)
	if month=="01":
		prev_month = "12"
	
	mark_attendance()
	make_leave_application()

	# process payroll
	if not frappe.db.get_value("Salary Slip", {"month": prev_month, "fiscal_year": year}):
		process_payroll = frappe.get_doc("Process Payroll", "Process Payroll")
		process_payroll.company = frappe.flags.company
		process_payroll.month = prev_month
		process_payroll.fiscal_year = year
		process_payroll.create_sal_slip()
		process_payroll.submit_salary_slip()
		r = process_payroll.make_journal_entry(frappe.get_value('Account',
			{'account_name': 'Salary'}))

		journal_entry = frappe.get_doc(r)
		journal_entry.cheque_no = random_string(10)
		journal_entry.cheque_date = frappe.flags.current_date
		journal_entry.posting_date = frappe.flags.current_date
		journal_entry.insert()
		journal_entry.submit()
	
	if frappe.db.get_global('demo_hr_user'):
		make_timesheet_records()
	
		#expense claim
		expense_claim = frappe.new_doc("Expense Claim")
		expense_claim.extend('expenses', get_expenses())
		expense_claim.employee = get_random("Employee")
		expense_claim.company = frappe.flags.company
		expense_claim.posting_date = frappe.flags.current_date
		expense_claim.exp_approver = filter((lambda x: x[0] != 'Administrator'), get_expense_approver(None, '', None, 0, 20, None))[0][0]
		expense_claim.insert()

		rand = random.random()

		if rand < 0.4:
			expense_claim.approval_status = "Approved"
			update_sanctioned_amount(expense_claim)
			expense_claim.submit()

			if random.randint(0, 1):
				#make journal entry against expense claim
				je = frappe.get_doc(make_bank_entry(expense_claim.name))
				je.posting_date = frappe.flags.current_date
				je.cheque_no = random_string(10)
				je.cheque_date = frappe.flags.current_date
				je.flags.ignore_permissions = 1
				je.submit()

		elif rand < 0.2:
			expense_claim.approval_status = "Rejected"
			expense_claim.submit()

def get_expenses():
	expenses = []
	expese_types = frappe.db.sql("""select ect.name, eca.default_account from `tabExpense Claim Type` ect,
		`tabExpense Claim Account` eca where eca.parent=ect.name
		and eca.company=%s """, frappe.flags.company,as_dict=1)

	for expense_type in expese_types[:random.randint(1,4)]:
		claim_amount = random.randint(1,20)*10

		expenses.append({
			"expense_date": frappe.flags.current_date,
			"expense_type": expense_type.name,
			"default_account": expense_type.default_account or "Miscellaneous Expenses - WPL",
			"claim_amount": claim_amount,
			"sanctioned_amount": claim_amount
		})

	return expenses

def update_sanctioned_amount(expense_claim):
	for expense in expense_claim.expenses:
		sanctioned_amount = random.randint(1,20)*10

		if sanctioned_amount < expense.claim_amount:
			expense.sanctioned_amount = sanctioned_amount

def get_timesheet_based_salary_slip_employee():
	sal_struct = frappe.db.sql("""
			select name from `tabSalary Structure`
			where salary_slip_based_on_timesheet = 1
			and docstatus != 2""")
	if sal_struct:
		employees = frappe.db.sql("""
				select employee from `tabSalary Structure Employee`
				where parent IN %(sal_struct)s""", {"sal_struct": sal_struct}, as_dict=True)
		return employees
	
def make_timesheet_records():
	employees = get_timesheet_based_salary_slip_employee()
	for e in employees:
		ts = make_timesheet(e.employee, simulate = True, billable = 1, activity_type=get_random("Activity Type"))

		rand = random.random()
		if rand >= 0.3:
			make_salary_slip_for_timesheet(ts.name)

		rand = random.random()
		if rand >= 0.2:
			make_sales_invoice_for_timesheet(ts.name)

def make_salary_slip_for_timesheet(name):
	salary_slip = make_salary_slip(name)
	salary_slip.insert()
	salary_slip.submit()
	frappe.db.commit()

def make_sales_invoice_for_timesheet(name):
	sales_invoice = make_sales_invoice(name)
	sales_invoice.customer = get_random("Customer")
	sales_invoice.append('items', {
		'item_code': get_random("Item", {"has_variants": 0, "is_stock_item": 0, "is_fixed_asset": 0}),
		'qty': 1,
		'rate': 1000
	})
	sales_invoice.flags.ignore_permissions = 1
	sales_invoice.set_missing_values()
	sales_invoice.calculate_taxes_and_totals()
	sales_invoice.insert()
	sales_invoice.submit()
	frappe.db.commit()
	
def make_leave_application():
	allocated_leaves = frappe.get_all("Leave Allocation", fields=['employee', 'leave_type'])
	
	for allocated_leave in allocated_leaves:
		leave_balance = get_leave_balance_on(allocated_leave.employee, allocated_leave.leave_type, frappe.flags.current_date,
			consider_all_leaves_in_the_allocation_period=True)
		if leave_balance != 0:
			if leave_balance == 1:
				to_date = frappe.flags.current_date
			else:
				to_date = add_days(frappe.flags.current_date, random.randint(0, leave_balance-1))
				
			leave_application = frappe.get_doc({
				"doctype": "Leave Application",
				"employee": allocated_leave.employee,
				"from_date": frappe.flags.current_date,
				"to_date": to_date,
				"leave_type": allocated_leave.leave_type,
				"status": "Approved"
			})
			try:
				leave_application.insert()
				leave_application.submit()
				frappe.db.commit()
			except (OverlapError):
				frappe.db.rollback()
			
def mark_attendance():
	att_date = frappe.flags.current_date
	for employee in frappe.get_all('Employee', fields=['name'], filters = {'status': 'Active'}):
		
		if not frappe.db.get_value("Attendance", {"employee": employee.name, "att_date": att_date}):
			attendance = frappe.get_doc({
				"doctype": "Attendance",
				"employee": employee.name,
				"att_date": att_date
			})
			leave = frappe.db.sql("""select name from `tabLeave Application`
				where employee = %s and %s between from_date and to_date and status = 'Approved'
				and docstatus = 1""", (employee.name, att_date))
			
			if leave:
				attendance.status = "Absent"
			else:
				attendance.status = "Present"
			attendance.save()
			attendance.submit()		
			frappe.db.commit()

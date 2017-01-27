NERP HR Documentation

#Taxation Unit:

Currently we have two main type of tax deduction:
1. Social Security Tax
2. Remunaration Tax

Note: You should create these two types model with same name to record its detail per employee.


#Report caveat:
In report setting table should be restricted to above conditions.

#Branch:
Branch option will appear according to payroll accountant hierarchy.


# Fixture install order:
**--> BranchOffice
**--> account.Category --> PayrollConfig
**--> hr.EmployeeGradeGroup --> hr.EmployeeGrade --> hr.Designation
**--> Group --> Users

#HR Required Groups:
1. Accountant and Payroll Accountant
2. Payroll Accountant for branch so (Payroll Accountant of which branch is to be specified)


# Employee model grade_number note
* grade_number field in Employee model represents the max grade the employee can use.
* scale_start_date should be available for all employee either from middle or from start.

# Set other units of calculation
1. Set some allowances
2. Set some deductions
3. set some facilities
3.
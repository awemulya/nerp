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

#HR Required Groups:
1. Accountant and Payroll Accountant
2. Payroll Accountant for branch so (Payroll Accountant of which branch is to be specified)


# Fixture install order:
**--> BranchOffice
**--> account.Category --> PayrollConfig
**--> hr.EmployeeGradeGroup --> hr.EmployeeGrade --> hr.Designation
**--> Group --> Users

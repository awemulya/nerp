def get allowance_details(**kwargs):
	allowance = 0
    employee_response['allowance_details'] =[]
    allowance_details = employee_response['allowance_details']
    for _name in employee.allowances.all():
        try:
            obj = _name.allowances.all().filter(
	            	employee_grade=employee.designation.grade,
	            	validity_id=kwargs['validity_id']
            	)[0]
        except IndexError:
            raise IndexError('%s not defined for grade %s' % (_name.name, employee.designation.grade.grade_name))
        # if obj:
        #     obj = obj[0]
        if obj.payment_cycle == 'Y':
            # check obj.year_payment_cycle_month to add to salary
            cnt = month_cnt_inrange(
                obj.year_payment_cycle_month,
                paid_from_date,
                paid_to_date
            )
            if cnt:
                if obj.sum_type == 'AMOUNT':
                    allowance_details.append({
                        'amount': obj.value * cnt
                    })
                else:
                    allowance_details.append({
                        'amount': obj.value / 100.0 * scale_salary
                    })
            else:
                allowance_details.append({
                    'amount': 0
                })

        elif obj.payment_cycle == 'M':
            if obj.sum_type == 'AMOUNT':
                allowance_details.append({
                    'amount': obj.value * total_month
                })
            else:
                allowance_details.append({
                    'amount': obj.value / 100.0 * scale_salary
                })
        elif obj.payment_cycle == 'D':
            if obj.sum_type == 'AMOUNT':
                allowance_details.append({
                    'amount': obj.value * total_work_day
                })
            else:
                allowance_details.append({
                    'amount':obj.value / 100.0 * scale_salary
                })
                # Does this mean percentage in daily wages
                # else:
                #     # This is hourly case(Dont think we have it)
                #     pass
                # else:
                #     # Here also same as below
                #     employee_response['allowance_%d' % (_name.id)] = 0
        allowance_details[-1]['allowance'] = _name.id
        allowance_details[-1]['name'] = _name.name
        allowance += allowance_details[-1]['amount']

    employee_response['allowance'] = allowance

def get_deduction_details():
    pass


def get_insentive_details():
    pass

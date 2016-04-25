// ko.bindingHandlers.customValVis = {
//     init: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
//         console.log('We are here in init');

//         var value = valueAccessor();
//         var valueUnwrapped = ko.unwrap(value);
//         var ufn = allBindings.get('parentFieldName')
//         console.log(bindingContext.$root[ufn]());
//         value(bindingContext.$root[ufn])
//         // This will be called when the binding is first applied to an element
//         // Set up any initial state, event handlers, etc. here
//     },
//     update: function(element, valueAccessor, allBindings, viewModel, bindingContext) {
//         console.log('We are here');
//         var value = valueAccessor();
//         var valueUnwrapped = ko.unwrap(value);
//         var ufn = allBindings.get('updateFieldName')
//         value(bindingContext.$root[ufn])
//         // var duration = allBindings.get('valueUpdate')
//     }
// };


$(document).ready(function () {
    vm = new PayrollEntry();
    ko.applyBindings(vm);
    // $('.change-on-ready').trigger('change');
    // $('.dropdown-menu').click(function (event) {
    //     event.stopPropagation();
    // });
});

function Transaction(){
    var self = this;
    self.account_id = ko.observable();
    self.debit = ko.observable();
    self.credit = ko.observable();
    self.description = ko.observable();
};


function PaymentEntryRow() {
    //debugger;
    var self = this;
    self.id = ko.observable();
    self.paid_employee = ko.observable();
    self.paid_from_date = ko.observable();
    self.paid_to_date = ko.observable();
    self.absent_days = ko.observable();
    self.allowance = ko.observable();
    self.incentive = ko.observable();
    self.deduced_amount = ko.observable();
    self.income_tax = ko.observable();
    self.pro_tempore_amount = ko.observable();
    self.salary = ko.observable();
    self.paid_amount = ko.observable();
    self.transactions = ko.observableArray();
    
    // Make here a observable function dat will set other parameters with employee id and date range
    self.setOtrParam = ko.computed(function(){
        if(self.paid_employee() && self.paid_from_date() && self.paid_to_date() && vm.payroll_type()=="INDIVIDUAL" ){
        $.ajax({
            url: 'get_employee_account/',
            method: 'POST',
            dataType: 'json',
            data: {
                paid_employee: self.paid_employee(),
                paid_from_date: self.paid_from_date(),
                paid_to_date: self.paid_to_date()
            },
            // async: true,
            success: function (response) {
                console.log(response);
                if(response.errors){
                    vm.paid_from_date_error(response.errors.paid_from_date)
                    vm.paid_to_date_error(response.errors.paid_to_date)
                }else{

                    self.allowance(response.data.allowance);
                    self.incentive(response.data.incentive);
                    self.deduced_amount(response.data.deduced_amount);
                    self.income_tax(response.data.income_tax);
                    self.pro_tempore_amount(response.data.pro_tempore_amount);
                    self.salary(response.data.salary);
                    self.paid_amount(response.data.paid_amount);

            // // Set transaction class here
            //         var company_credit_trans = function(credit_amount, description){
            //             var company_trans = new Transaction()
            //             company_trans.account_id = response.data.salary_giving_account_id;
            //             company_trans.credit = credit_amount;
            //             company_trans.debit = 0;
            //             company_trans.description = description;
            //             self.transactions.push(company_trans);
            //         };
            //     // User account debit transaction
                    
            //         // Salary + Allowance Transaction
            //         var sal_all_tran = new Transaction();
            //         sal_all_tran.account_id = response.data.employee_bank_account_id;
            //         sal_all_tran.debit = self.salary() + self.allowance();
            //         sal_all_tran.credit = 0;
            //         sal_all_tran.description = 'Salary + allowance amount:';
                    
            //         company_credit_trans(
            //             sal_all_tran.debit,
            //             sal_all_tran.description + 'to EmployeeID#' + String(paid_employee());
            //          );
                    
            //         self.transactions.push(sal_all_tran);

            //         // Incentive Transaction
            //         if(self.incentive() > 0){
            //             var incentive_tran = new Transaction();
            //             incentive_tran.account_id = response.data.employee_bank_account_id;
            //             incentive_tran.debit = self.incentive();
            //             incentive_tran.credit = 0;
            //             incentive_tran.description = 'Employee Incentive Payment';
                        
            //             company_credit_trans(
            //                 incentive_tran.debit,
            //                 sal_.description + 'to EmployeeID#' + String(paid_employee());
            //             );

            //             self.transactions.push(incentive_tran);
            //         };

            //         // Pro tempore Transaction
            //         if(self.pro_tempore_amount() > 0){
            //             var prot_tran = new Transaction();
            //             prot_tran.account_id = response.data.employee_bank_account_id;
            //             prot_tran.debit = self.pro_tempore_amount();
            //             prot_tran.credit = 0;
            //             prot_tran.description = 'Pro Tempore Amount Payment';
            //             self.transactions.push(prot_tran);
            //         };
            //     // Employee Account Credit Transaction OR Deductions
            //         for(deduction of response.deduction_detail){
            //             var deduct_transaction = new Transaction()
            //             var bank_transaction = new Transaction()
            //             for(dat of deduction){
            //                 deduct_transaction.account_id = dat.account_id;
            //                 deduct_transaction.debit = dat.amount;
            //                 bank_transaction.account_id = response.data.employee_bank_account_id;
            //                 bank_transaction.credit = dat.amount;
            //             };
            //             deduct_transaction.credit = 0;
            //             bank_transaction.debit = 0;
            //             deduct_transaction.description = 'Pro Tempore Amount Payment';
            //             bank_transaction.description = 'Pro Tempore Amount Payment';
            //             self.transactions.push(deduct_transaction);
            //             self.transactions.push(bank_transaction);
            //         };



                };
            },
            error: function(errorThrown){
                console.log(errorThrown);
                },
//            self.budget_heads = ko.observableArray(data);
        });
            console.log('Here get other computed data from the server')
        }else{
            console.log('Those three attributes are not set')
        };
    });

};

function PayrollEntry() {
    //debugger;
    var self = this;
    self.payroll_type = ko.observable();
    self.rows = ko.observableArray([]);
    // self.id = ko.observable();
    self.paid_from_date = ko.observable();
    self.paid_to_date = ko.observable();

    self.paid_from_date_error = ko.observable();
    self.paid_to_date_error = ko.observable();

    // self.entry_datetime=ko.observable();
    self.branch = ko.observable();
    
    self.switch_p_type  = ko.computed(function(){
        console.log(self.payroll_type)
        if(self.payroll_type()=="INDIVIDUAL"){
            if( self.rows().length == 0){    
                self.rows.push(new PaymentEntryRow())
            };
            return true;
        }else{
            self.rows([])
            return false;
        };
    }); 

    self.saveAndAdd = function(){
        console.log('payment row saved');
    };
    self.setup_formset = function(){
        row_elements = $('.payment-row-table').children().children()
        for(i=2; i<row_elements.length;i++ ){
            ele = $(row_elements[i]).children();
            for(j=0; j<ele.length-1;j++){
                input_element = $(ele[j]).children()[0];
                name_attr = $(input_element).attr('name');
                id_attr = $(input_element).attr('id');
                name_split = name_attr.split('-');
                name_split[1] = String(i-1)
                id_split = id_attr.split('-');
                id_split[1] = String(i-1) 
                $(input_element).attr('name', name_split.join('-'));
                $(input_element).attr('id', id_split.join('-'));
            };

        };
    };
    self.addRow = function(event){
        self.rows.push(new PaymentEntryRow());
        self.setup_formset();
    };
    self.removeRow = function(row){
        self.rows.remove(row);
        self.setup_formset();
    };
    self.set_time_stamp = ko.computed(function(){
        // console.log('We are in timestamp function');
        if(self.paid_from_date() && self.paid_to_date()){
            for(let o of self.rows()){
                // console.log(self.paid_from_date());
                // console.log(self.paid_to_date());
                o.paid_from_date(self.paid_from_date());
                o.paid_to_date(self.paid_to_date());
                // console.log('value set')
            };
        };
    });
    self.getGroupSalary = function(){
        $.ajax({
            url: 'get_employees_account/',
            method: 'POST',
            dataType: 'json',
            data: {
                branch: self.branch(),
                paid_from_date: self.paid_from_date(),
                paid_to_date: self.paid_to_date()
            },
            // async: true,
            success: function (response) {
                if(response.errors){
                    self.paid_from_date_error(response.errors.paid_from_date)
                    self.paid_to_date_error(response.errors.paid_to_date)
                }else{
                    console.log(response);
                    self.rows([]);
                    for(data of response.data){
                        var row = new PaymentEntryRow()
                        row.paid_employee(data.employee_id);
                        row.allowance(data.allowance);
                        row.incentive(data.incentive);
                        row.deduced_amount(data.deduced_amount);
                        row.income_tax(data.income_tax);
                        row.pro_tempore_amount(data.pro_tempore_amount);
                        row.salary(data.salary);
                        row.paid_amount(data.paid_amount);
                        self.rows.push(row);
                    }
                };

                // Here mapping should be done
                // console.log(data);
            },
            error: function(errorThrown){
                console.log(errorThrown);
            },
//            self.budget_heads = ko.observableArray(data);
        });
    };
    
    

};



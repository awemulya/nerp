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
    vm = new PayrollEntry(ko_data);
    ko.applyBindings(vm);
    // $('.change-on-ready').trigger('change');
    // $('.dropdown-menu').click(function (event) {
    //     event.stopPropagation();
    // });
});

function PaymentRowWitDeduction(pwd_data){
    if(pwd_data.deduction_data){
        var PER = new PaymentEntryRow();
        var DeductionPER = ko.mapping.fromJS(pwd_data.deduction_data);
        return $.extend(PER, DeductionPER);
    }else{
        var PER = new PaymentEntryRow();
        return PER;
    };
    // var self = this;
    // self.deduction_id = ko.observable();
    // self.name = ko.observable();
    // self.amount = ko.observable();
    // // self.credit = ko.observable();
    // // self.description = ko.observable();
};


function PaymentEntryRow(data) {
    //debugger;
    var self = this;
    self.id = ko.observable();
    self.paid_employee = ko.observable();

    self.employee_grade = ko.observable();
    self.employee_designation = ko.observable();

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
    self.request_flag = ko.observable(true);
    self.row_error = ko.observable('');
    
    // self.deduction_detail = ko.observableArray();
    // here we will do mapping instead
    

    self.employee_changed = function () {
        console.log('We entered here successfully');
        console.log(self.paid_employee())
        self.request_flag(true); 
        // self.setOtrParam();   
        // if (event.originalEvent) { //user changed
        // } else { // program changed
    };


    // Make here a observable function dat will set other parameters with employee id and date range
    self.setOtrParam = ko.computed(function(){
        if(self.paid_employee() && self.paid_from_date() && self.paid_to_date() && vm.payroll_type()=="INDIVIDUAL" && self.request_flag){
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
                    var mapping = {
                        'ignore': ["paid_employee"]
                    }
                    self.request_flag(false);
                    ko.mapping.fromJS(response.data, mapping, self);
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

function PayrollEntry(pr_data) {
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

    self.deduction_headings = ko.observableArray();
    
    self.switch_p_type  = ko.computed(function(){
        if(self.payroll_type()=="INDIVIDUAL"){
            return true;
        }else{
            return false;
        };
    }); 

    self.clear_row = ko.computed(function(){
        if(self.switch_p_type() == true){
            self.rows([]);
            self.rows.push(PaymentRowWitDeduction(pr_data));
            
        }else{
            self.rows([]);
        };
    });

    self.saveAndAdd = function(formElement){
        console.log('payment row saved');
    };
    self.setup_formset = function(){
        row_elements = $('.payment-row-table').children().children()
        for(i=2; i<row_elements.length;i++ ){
            ele = $(row_elements[i]).children();
            for(j=0; j<ele.length-1;j++){
                input_element = $(ele[j]).children()[0];
                
                name_attr = $(input_element).attr('name');
                if(name_attr){    
                    name_split = name_attr.split('-');
                    name_split[1] = String(i-1)
                    $(input_element).attr('name', name_split.join('-'));
                };
                
                id_attr = $(input_element).attr('id');
                if(id_attr){    
                    id_split = id_attr.split('-');
                    id_split[1] = String(i-1) 
                    $(input_element).attr('id', id_split.join('-'));
                };
                
            };

        };
    };
    self.addRow = function(event){
        self.rows.push(new PaymentRowWitDeduction(pr_data));
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
                        // var row = new PaymentRowWitDeduction(data);
                        // var mapping = {
                        // 'employee_changed': function(){},
                        // };
                        var row = ko.mapping.fromJS(data);
                        row.paid_from_date = ko.observable();
                        row.paid_to_date = ko.observable();
                        row.employee_changed = function(){};
                        if(typeof(row.row_error)=='undefined'){
                            row.row_error = ko.observable('');
                        };
                        // row.paid_employee(data.employee_id);
                        // row.allowance(data.allowance);
                        // row.incentive(data.incentive);
                        // row.deduced_amount(data.deduced_amount);
                        // row.income_tax(data.income_tax);
                        // row.pro_tempore_amount(data.pro_tempore_amount);
                        // row.salary(data.salary);
                        // row.paid_amount(data.paid_amount);
                        self.rows.push(row);
                    }
                };
                self.setup_formset();

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



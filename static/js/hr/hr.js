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


function PaymentEntryRow(per_data) {
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
    self.row_errors = ko.observableArray();
    
    // self.employee_counter = ko.observable(0);
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
                paid_to_date: self.paid_to_date(),
                monthly_payroll: vm.monthly_payroll()
            },
            // async: true,
            success: function (response) {
                console.log(response);
                if(response.errors){
                    // vm.paid_from_date_error(response.errors.paid_from_date)
                    // vm.paid_to_date_error(response.errors.paid_to_date)
                    vm.rows([PaymentRowWitDeduction(ko_data),]);
                    // vm.rows([]);
                    if(response.errors.paid_from_date){
                        vm.paid_from_date_error(response.errors.paid_from_date);
                    }else{
                        vm.paid_from_date_error(null);
                    };
                    if(response.errors.paid_to_date){
                        vm.paid_to_date_error(response.errors.paid_to_date);
                    }else{
                        vm.paid_to_date_error(null);
                    };
                    if(response.errors.invalid_date_range){
                        vm.invalid_date_range(response.errors.invalid_date_range);
                    }else{
                        vm.invalid_date_range(null);
                    };
                }else{
                    vm.paid_from_date_error(null);
                    vm.paid_to_date_error(null);
                    vm.invalid_date_range(null);
                    var mapping = {
                        'ignore': ["paid_employee"]
                    }
                    self.request_flag(false);
                    
                    ko.mapping.fromJS(response.data, mapping, self);
                    if(typeof(response.data.row_errors)=='undefined'){
                        self.row_errors([]);
                    }
                    
                    // if(vm.rows.length == 1){
                        vm.paid_from_date(response.data.paid_from_date);
                        vm.paid_to_date(response.data.paid_to_date);
                    // };
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

    self.invalid_date_range = ko.observable();

    self.monthly_payroll = ko.observable(true);

    // self.entry_datetime=ko.observable();
    self.branch = ko.observable();

    // self.deduction_headings = ko.observableArray();

    self.messages = ko.observableArray();
    
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

    self.m_p_changed = ko.computed(function(){
        self.monthly_payroll();
        if(self.payroll_type() == 'INDIVIDUAL'){
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
        var row_elements = $('.payment-row-table').children().children();
        var cntr = 0;
        for(i=1; i<row_elements.length;i++ ){
            var ele = $(row_elements[i]).children();
            if(ele.children().length == 0){continue;};
            for(j=0; j<ele.length-1;j++){
                var input_element = $(ele[j]).children()[0];
                var name_attr = $(input_element).attr('name');
                if(name_attr){    
                    var name_split = name_attr.split('-');
                    name_split[1] = String(cntr);
                    $(input_element).attr('name', name_split.join('-'));

                };
                
                var id_attr = $(input_element).attr('id');
                if(id_attr){    
                    var id_split = id_attr.split('-');
                    id_split[1] = String(cntr); 
                    $(input_element).attr('id', id_split.join('-'));
                };
                
            };
            cntr ++;

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
        console.log('We are in timestamp function');
        if(self.payroll_type() != 'GROUP'){
            
            if(self.paid_from_date() && self.paid_to_date()){
                for(let o of self.rows()){
                    // console.log(self.paid_from_date());
                    // console.log(self.paid_to_date());
                    o.paid_from_date(self.paid_from_date());
                    o.paid_to_date(self.paid_to_date());
                    // console.log('value set')
                };
            };
        };
    });

    self.group_date_update = ko.computed(function(){
        alert('Group date update');
        if(self.payroll_type() == 'GROUP'){
            var has_error = false;
            for(ro of self.rows()){
                if(self.paid_from_date() != ro.paid_from_date() || self.paid_to_date() != ro.paid_to_date()){
                    has_error = true;
                    self.messages.push('Your date range has been updated. Press Get Salary button to get updated values');
                    break;
                };
            };
            if(!has_error){
                self.messages([]);
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
                paid_to_date: self.paid_to_date(),
                monthly_payroll: self.monthly_payroll()
            },
            // async: true,
            success: function (response) {
                if(response.errors){
                    self.rows([]);
                    if(response.errors.paid_from_date){
                        self.paid_from_date_error(response.errors.paid_from_date);
                    }else{
                        self.paid_from_date_error(null);
                    };
                    if(response.errors.paid_to_date){
                        self.paid_to_date_error(response.errors.paid_to_date);
                    }else{
                        self.paid_to_date_error(null);
                    };
                    if(response.errors.invalid_date_range){
                        self.invalid_date_range(response.errors.invalid_date_range);
                    }else{
                        self.invalid_date_range(null);
                    };

                }else{
                    self.paid_from_date_error(null);
                    self.paid_to_date_error(null);
                    self.invalid_date_range(null);


                    console.log(response);
                    self.rows([]);

                    var c = 0;
                    for(data of response.data){
                        c += 1;
                        // var row = new PaymentRowWitDeduction(data);
                        // var mapping = {
                        // 'employee_changed': function(){},
                        // };
                        var row = ko.mapping.fromJS(data);
                        // We wont need this if server throws the date
                        // row.paid_from_date = ko.observable();
                        // row.paid_to_date = ko.observable();
                        row.employee_changed = function(){};
                        if(typeof(row.row_errors)=='undefined'){
                            row.row_errors = ko.observableArray([]);
                        };
                        if(c==1){
                            self.paid_from_date(row.paid_from_date());
                            self.paid_to_date(row.paid_to_date());
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



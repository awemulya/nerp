$(document).ready(function () {

    vm = new PayrollEntry(ko_data);
    ko.applyBindings(vm);
});

function PaymentRowWitDeduction(pwd_data){
    var extract_obsevable_name = function(ko_obj, dict_output){
        var observabe_names = {};
        var observable_list = [];
        ko_obj.forEach(function(obj){
            observabe_names[obj.observable_name] = 0;
            observable_list.push(obj.observable_name);
        });
        if (dict_output){
            return observabe_names;
        }else{
            return observable_list;
        }
    };
    var PER = new PaymentEntryRow();
    if(pwd_data.deduction_data){
        var DeductionPER = ko.mapping.fromJS(extract_obsevable_name(pwd_data.deduction_data, true));
        $.extend(PER, DeductionPER);
    }

    if(pwd_data.incentive_data){
        var IncentivePER = ko.mapping.fromJS(extract_obsevable_name(pwd_data.incentive_data, true));
        $.extend(PER, IncentivePER);
    }
    if(pwd_data.allowance_data){
        var AllowancePER = ko.mapping.fromJS(extract_obsevable_name(pwd_data.allowance_data, true));
        $.extend(PER, AllowancePER);
    }
    
    PER.compute_editable_totals = ko.computed(function(){
        var total_deduction = 0;
        var total_incentive = 0;

        var extracted_deduction_obs_names = extract_obsevable_name(pwd_data.deduction_data, false);
        extracted_deduction_obs_names.forEach(function(obj){
           total_deduction += parseInt(PER[obj]());
        });

        var extracted_incentive_obs_names = extract_obsevable_name(pwd_data.incentive_data, false);

        extracted_incentive_obs_names.forEach(function(obj){
            total_incentive += parseInt(PER[obj]());
        });
        PER.deduced_amount(total_deduction);
        PER.incentive(total_incentive);
        var total_paid_amount = PER.salary() - PER.deduced_amount() - PER.income_tax() + PER.pro_tempore_amount() + PER.incentive() + PER.allowance();
        PER.paid_amount(total_paid_amount);
    });
    
    return PER;
};


function PaymentEntryRow() {
    var self = this;
    self.id = ko.observable();
    self.paid_employee = ko.observable();

    self.employee_grade = ko.observable();
    self.employee_designation = ko.observable();

    self.paid_from_date = ko.observable();
    self.paid_to_date = ko.observable();
    self.absent_days = ko.observable(0);
    self.allowance = ko.observable(0);
    self.incentive = ko.observable(0);
    self.deduced_amount = ko.observable(0);
    self.income_tax = ko.observable(0);
    self.pro_tempore_amount = ko.observable(0);
    self.salary = ko.observable(0);
    self.paid_amount = ko.observable(0);
    self.request_flag = ko.observable(true);
    self.row_errors = ko.observableArray();
    self.disable_input = ko.observable(false);

    self.emp_options = ko.observableArray();

    self.employee_changed = function () {
        // console.log('We entered here successfully');
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
                    // vm.selected_employees([]);
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
                        vm.messages.push(response.errors.invalid_date_range);
                    };
                }else{
                    vm.paid_from_date_error(null);
                    vm.paid_to_date_error(null);
                    // vm.invalid_date_range(null);
                    var mapping = {
                        'ignore': ["paid_employee", "emp_options"]
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
            // console.log('Here get other computed data from the server')
        }else{
            // console.log('Those three attributes are not set')
        };
    });

};

function PayrollEntry(pr_data) {
    //debugger;
    var self = this;

    self.entry_id = ko.observable();
    self.entry_saved = ko.observable(false);
    self.entry_approved = ko.observable(false);
    self.entry_transacted = ko.observable(false);

    self.approve_entry = function(){
        $.ajax({
                url: 'approve_entry/' + String(self.entry_id()),
                method: 'GET',
                dataType: 'json',
                // data: post_data,
                // async: true,
                success: function (response) {
                    console.log(response);
                    self.entry_approved(response.entry_approved);
                    
                },
                error: function(errorThrown){
                    console.log(errorThrown);
                    },
    //            self.budget_heads = ko.observableArray(data);
            });

    };
    self.transact = function(){
        $.ajax({
                url: '/payroll/transact_entry/' + String(self.entry_id()),
                method: 'GET',
                dataType: 'json',
                // data: post_data,
                // async: true,
                success: function (response) {
                    console.log(response);
                    self.entry_transacted(true);
                    // self.entry_approved(response.entry_approved);
                    
                },
                error: function(errorThrown){
                    console.log(errorThrown);
                    },
    //            self.budget_heads = ko.observableArray(data);
        });
    };
    // self.entry_delete = function(){
    //     $.ajax({
    //             url: 'delete_entry/' + String(self.entry_id()),
    //             method: 'GET',
    //             dataType: 'json',
    //             // data: post_data,
    //             // async: true,
    //             success: function (response) {
    //                 console.log(response);
                    
                    
    //             },
    //             error: function(errorThrown){
    //                 console.log(errorThrown);
    //                 },
    // //            self.budget_heads = ko.observableArray(data);
    //         });
    // };

    self.payroll_type = ko.observable();
    self.rows = ko.observableArray([]);
    // self.id = ko.observable();
    self.paid_from_date = ko.observable();
    self.paid_to_date = ko.observable();

    self.paid_from_date_error = ko.observable();
    self.paid_to_date_error = ko.observable();

    // self.invalid_date_range = ko.observable();

    self.monthly_payroll = ko.observable(true);

    // self.entry_datetime=ko.observable();
    self.branch = ko.observable();

    // self.deduction_headings = ko.observableArray();

    self.messages = ko.observableArray();

    self.employee_options = ko.observableArray();
    
    self.switch_p_type  = ko.computed(function(){
        if(self.payroll_type()=="INDIVIDUAL"){
            return true;
        }else{
            return false;
        };
    }); 

    // self.clear_row = ko.computed(function(){
    //     if(self.switch_p_type() == true){
    //         self.rows([]);
    //         self.rows.push(PaymentRowWitDeduction(pr_data));
            
    //     }else{
    //         self.rows([]);
    //     };
    // });

    self.m_p_changed = ko.computed(function(){
        // self.monthly_payroll();
        if(self.payroll_type() == 'INDIVIDUAL'){
            self.rows([]);
            self.rows.push(PaymentRowWitDeduction(pr_data));
        }else{
            self.rows([]);
        };
    });

    
    // Data Changing parameters when changed should reser self.save, approve,transact to default
    self.set_save_param_to_default = function(){
        self.entry_id = ko.observable();
        self.entry_saved(false);
        self.entry_approved(false);
        self.entry_transacted(false);
    };


    self.saveAndAdd = function(formElement){
        var has_error = false;
        for(var row of self.rows()){
            if(row.row_errors().length > 0){
                // here has true should be true 
                has_error = true;
                self.messages.push('Remove rows with warnings to Save the entry');
            };
        };
        if(!has_error){
            $.ajax({
                url: 'save_payroll_entry/',
                method: 'POST',
                dataType: 'json',
                data: ko.toJSON(self),
                // async: true,
                success: function (response) {
                    console.log(response);
                    self.entry_id(response.entry_id);
                    self.entry_saved(response.entry_saved);
                    self.entry_approved(response.entry_approved);
                    self.entry_transacted(response.entry_transacted);
                    
                },
                error: function(errorThrown){
                    console.log(errorThrown);
                    },
    //            self.budget_heads = ko.observableArray(data);
            });
        };
    };

    self.addRow = function(event){
        self.rows.push(new PaymentRowWitDeduction(pr_data));
    };
    self.removeRow = function(row){
        self.rows.remove(row);
    };
    self.set_time_stamp = ko.computed(function(){
        console.log('We are in timestamp function');
        if(self.payroll_type() != 'GROUP'){
            
            if(self.paid_from_date() && self.paid_to_date()){
                for(var o of self.rows()){
                    // console.log(self.paid_from_date());
                    // console.log(self.paid_to_date());
                    o.paid_from_date(self.paid_from_date());
                    o.paid_to_date(self.paid_to_date());
                    // console.log('value set')
                };
            };
        };
    });

    // self.group_date_update = ko.computed(function(){
        
    //     if(self.payroll_type() == 'GROUP'){
    //         var has_error = false;
    //         for(ro of self.rows()){
    //             if(self.paid_from_date() != ro.paid_from_date() || self.paid_to_date() != ro.paid_to_date()){
    //                 has_error = true;
    //                 self.getGroupSalary();
    //                 break;
    //             };
    //         };
    //         if(!has_error){
    //             self.messages([]);
    //         };
    //     };
    // });

    // self.group_changed = function(){
    //     if(self.payroll_type() == 'GROUP'){
    //         self.getGroupSalary()
    //     }else{
    //         // Update employee options
    //     };
    // };
     
    // self.disable_input = ko.computed(function(){
    //     if(self.payroll_type() == 'GROUP'){
    //         return true;
    //     }else{
    //         return false;
    //     };
    // });

    self.getGroupSalary = function(){
        console.log('This is get group salary');
        if(self.payroll_type() == 'GROUP')
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
                        self.messages.push(response.errors.invalid_date_range);
                    };

                }else{
                    self.paid_from_date_error(null);
                    self.paid_to_date_error(null);
                    // self.invalid_date_range(null);


                    console.log(response);
                    self.rows([]);

                    var c = 0;
                    for(var data of response.data){
                        c += 1;
                        // var row = new PaymentRowWitDeduction(data);
                        // var mapping = {
                        // 'employee_changed': function(){},
                        // };
                        var row = ko.mapping.fromJS(data);
                        // for(opt of row.emp_options()){
                        //     opt.id = opt.id();
                        //     opt.name = opt.name();
                        // };
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
            },
            error: function(errorThrown){
                console.log(errorThrown);
            },
        });
    };
    self.get_employee_options = ko.computed(function(){
        if(self.payroll_type() == 'INDIVIDUAL'){

            $.ajax({
                url: 'get_employee_options/',
                method: 'POST',
                dataType: 'json',
                data: {
                    branch: self.branch()? self.branch() : 'ALL'
                    // paid_from_date: self.paid_from_date(),
                    // paid_to_date: self.paid_to_date(),
                    // monthly_payroll: self.monthly_payroll()
                },
                // async: true,
                success: function (response) {
                    // for(row of self.rows()){
                    //     row.emp_options(response.opt_data);
                    // };
                    // debugger;
                //     for(emp of response.opt_data){
                //         emp.disable = ko.observable(false);
                //     };
                    self.employee_options(response.opt_data);
                },
                error: function(errorThrown){
                    console.log(errorThrown);
                    },
    //            self.budget_heads = ko.observableArray(data);
            });    
        };
    });
    // self.update_row_function = ko.computed(function(){
    //     if(self.rows()){
    //         for(row of self.rows()){
    //             row.emp_options(self.employee_options());
    //         };
    //     }
    // });
    // self.set_option_disable = function(option, item){
    //     if(typeof(item) != 'undefined'){
    //         ko.applyBindingsToNode(option, {disable: item.disable}, item);
    //     };
    // };
    // self.selected_employees = ko.observableArray();
    self.selected_employees = ko.computed(function(){
        var sel_e = [];
        for(row of self.rows()){
            if(typeof(row.paid_employee()) != 'undefined'){
                sel_e.push(row.paid_employee());
            };
        };
        return sel_e;
        // self.selected_employees(sel_e);
    });
    self.update_employee_options = ko.computed(function(){
        if(self.payroll_type() == 'INDIVIDUAL'){
            for(ro of self.rows()){
                ro.emp_options(self.employee_options().slice());
                var to_remove = []
                for(opt of ro.emp_options()){

                    if($.inArray(String(opt.id), self.selected_employees()) != -1 && String(opt.id) != ro.paid_employee()){                        
                        // console.log('To remove opt' + String(opt.id) + 'in loop' + String(loop_count) )
                        
                        to_remove.push(opt);
                        // console.log('removed opt' + String(opt.id) + 'in loop' + String(loop_count) )        
                    };
                };
                var diff = $(ro.emp_options()).not(to_remove).get();
                ro.emp_options(diff);
            };
        };
    });
    // Removes row with designation and grade and no employee selected
    self.del_row_ind_gc = ko.computed(function(){
        if(self.payroll_type() == 'INDIVIDUAL' && self.branch()){    
            for(var roo of self.rows()){
                if(!roo.paid_employee() && roo.employee_designation && roo.employee_grade()){
                    self.rows.remove(roo);
                            
                };
            };
            if(self.rows().length == 0){
                self.rows.push(new PaymentRowWitDeduction(pr_data));
            };
        };
    });
    self.remove_alert = function(alert_msg){
        console.log(alert_msg);
        self.messages.remove(alert_msg);
    };

};



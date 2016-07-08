$(document).ready(function () {

    vm = new PayrollEntry();
    ko.applyBindings(vm);
    if (ctx_data) {
        var mapping = {
            'entry_rows': {
                create: function (options) {
                    var entry_row = ko.mapping.fromJS(options.data, {}, new PaymentEntryRow());
                    if (typeof(options.parent.paid_from_date()) == 'undefined'){
                        debugger;
                        options.parent.paid_from_date(options.data.paid_from_date);
                        options.parent.paid_to_date(options.data.paid_to_date);
                    }
                    return entry_row
                }
            }
        };
        console.log('about to map on edit');
        ko.mapping.fromJS(ctx_data, mapping, vm);
    }
});

function PaymentEntryRow() {
    var self = this;
    self.id = ko.observable();
    // if(emp_options){
    self.emp_options = ko.observableArray();
    // }else{
    //     self.emp_options = ko.observableArray();
    // }
    self.emp_options = ko.observableArray();
    self.emp_options.extend({ notify: 'always' });
    self.paid_employee = ko.observable();
    self.employee_id = null;

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


    self.incentive_details = ko.observableArray();
    self.allowance_details = ko.observableArray();
    self.deduction_details = ko.observableArray();

    self.is_explicitly_added_row = ko.observable();

    // if (row_ctx_data) {
    //     ko.mapping.fromJS(row_ctx_data, {}, self);
    //     debugger;
    // }

    // self.employee_changed = function () {
    //     console.log(self.paid_employee());
    //     self.request_flag(true);
    // };
    self.paid_employee.subscribe(function () {
        console.log('This is paid employee')
        console.log(self.paid_employee());
        if (self.paid_employee()){
            self.employee_id = parseInt(self.paid_employee());
        }
        self.request_flag(true);
    });
    self.emp_options.subscribe(function(){
        self.paid_employee(self.employee_id);
    });

    // Make here a observable function dat will set other parameters with employee id and date range
    self.is_explicitly_added_row.subscribe(function () {
        if (self.paid_from_date() && self.paid_to_date() && self.request_flag && is_explicitly_added_row() && self.paid_employee()) {
            $.ajax({
                url: 'get_employee_account/',
                method: 'POST',
                dataType: 'json',
                data: {
                    paid_employee: self.paid_employee(),
                    paid_from_date: self.paid_from_date(),
                    paid_to_date: self.paid_to_date(),
                    is_monthly_payroll: vm.is_monthly_payroll()
                },
                // async: true,
                success: function (response) {
                    console.log(response);
                    if (response.errors) {
                        vm.entry_rows([PaymentEntryRow()]);
                        if (response.errors.paid_from_date) {
                            vm.paid_from_date_error(response.errors.paid_from_date);
                        } else {
                            vm.paid_from_date_error(null);
                        }

                        if (response.errors.paid_to_date) {
                            vm.paid_to_date_error(response.errors.paid_to_date);
                        } else {
                            vm.paid_to_date_error(null);
                        }
                        if (response.errors.invalid_date_range) {
                            vm.messages.push(response.errors.invalid_date_range);
                        }
                    } else {
                        vm.paid_from_date_error(null);
                        vm.paid_to_date_error(null);
                        // vm.invalid_date_range(null);
                        var mapping = {
                            'ignore': ["paid_employee", "emp_options"]
                        };
                        self.request_flag(false);

                        ko.mapping.fromJS(response.data, mapping, self);
                        if (typeof(response.data.row_errors) == 'undefined') {
                            self.row_errors([]);
                        }

                        // if(vm.entry_rows.length == 1){
                        vm.paid_from_date(response.data.paid_from_date);
                        vm.paid_to_date(response.data.paid_to_date);
                        // };
                    }

                },
                error: function (errorThrown) {
                    console.log(errorThrown);
                }
            });
        } else {
        }
    });

}

function PayrollEntry() {
    //debugger;
    var self = this;

    self.id = ko.observable();
    self.entry_saved = ko.observable(false);
    self.approved = ko.observable(false);
    self.transacted = ko.observable(false);

    self.payroll_type = ko.observable();
    self.entry_rows = ko.observableArray([]);
    // self.id = ko.observable();
    self.paid_from_date = ko.observable();
    self.paid_to_date = ko.observable();

    self.paid_from_date_error = ko.observable();
    self.paid_to_date_error = ko.observable();

    // self.invalid_date_range = ko.observable();

    self.is_monthly_payroll = ko.observable(true);

    // self.entry_datetime=ko.observable();
    self.branch = ko.observable();

    // self.deduction_headings = ko.observableArray();

    self.messages = ko.observableArray();

    self.employee_options = ko.observableArray();

    // self.id.subscribe(function(){
    //     if(self.id()){
    //         self.entry_saved(true);
    //     }
    // })

    self.approve_entry = function () {
        $.ajax({
            url: 'approve_entry/' + String(self.id()),
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                console.log(response);
                self.approved(response.approved);

            },
            error: function (errorThrown) {
                console.log(errorThrown);
            }
            //            self.budget_heads = ko.observableArray(data);
        });

    };
    self.transact = function () {
        $.ajax({
            url: '/payroll/transact_entry/' + String(self.id()),
            method: 'GET',
            dataType: 'json',
            success: function (response) {
                console.log(response);
                self.transacted(true);

            },
            error: function (errorThrown) {
                console.log(errorThrown);
            }
        });
    };
    // self.entry_delete = function(){
    //     $.ajax({
    //             url: 'delete_entry/' + String(self.id()),
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


    self.switch_p_type = ko.computed(function () {
        if (self.payroll_type() == "INDIVIDUAL") {
            return true;
        } else {
            return false;
        }

    });

    // self.clear_row = ko.computed(function(){
    //     if(self.switch_p_type() == true){
    //         self.entry_rows([]);
    //         self.entry_rows.push(PaymentRowWitDeduction(pr_data));

    //     }else{
    //         self.entry_rows([]);
    //     };
    // });

    self.payroll_type.subscribe(function () {
        // self.is_monthly_payroll();
        if (!self.id()) {
            if (self.payroll_type() == 'INDIVIDUAL') {
                self.entry_rows([]);
                self.entry_rows.push(new PaymentEntryRow());
            } else {
                self.entry_rows([]);
            }
        }

    });


    // Data Changing parameters when changed should reser self.save, approve,transact to default
    self.set_save_param_to_default = function () {
        self.id = ko.observable();
        self.entry_saved(false);
        self.approved(false);
        self.transacted(false);
    };


    self.saveAndAdd = function (formElement) {
        var has_error = false;
        for (var row of self.entry_rows()) {
            if (row.row_errors().length > 0) {
                // here has true should be true 
                has_error = true;
                self.messages.push('Remove rows with warnings to Save the entry');
            }
        }
        if (!has_error) {
            $.ajax({
                url: 'save_payroll_entry/',
                method: 'POST',
                dataType: 'json',
                data: ko.toJSON(self),
                // async: true,
                success: function (response) {
                    console.log(response);
                    self.id(response.id);
                    self.entry_saved(response.entry_saved);
                    self.approved(response.approved);
                    self.transacted(response.transacted);

                },
                error: function (errorThrown) {
                    console.log(errorThrown);
                }
                //            self.budget_heads = ko.observableArray(data);
            });
        }
    };

    self.addRow = function (event) {
        self.entry_rows.push(new PaymentEntryRow());
    };
    self.removeRow = function (row) {
        self.entry_rows.remove(row);
    };
    self.set_time_stamp = ko.computed(function () {
        console.log('We are in timestamp function');
        if (self.payroll_type() != 'GROUP') {

            if (self.paid_from_date() && self.paid_to_date()) {
                for (var o of self.entry_rows()) {
                    // console.log(self.paid_from_date());
                    // console.log(self.paid_to_date());
                    o.paid_from_date(self.paid_from_date());
                    o.paid_to_date(self.paid_to_date());
                    // console.log('value set')
                }
            }
        }
    });

    self.getGroupSalary = function () {
        console.log('This is get group salary');
        if (self.payroll_type() == 'GROUP')
            $.ajax({
                url: '/payroll/get_employees_account/',
                method: 'POST',
                dataType: 'json',
                data: {
                    branch: self.branch(),
                    paid_from_date: self.paid_from_date(),
                    paid_to_date: self.paid_to_date(),
                    is_monthly_payroll: self.is_monthly_payroll()
                },
                // async: true,
                success: function (response) {
                    if (response.errors) {
                        self.entry_rows([]);
                        if (response.errors.paid_from_date) {
                            self.paid_from_date_error(response.errors.paid_from_date);
                        } else {
                            self.paid_from_date_error(null);
                        }

                        if (response.errors.paid_to_date) {
                            self.paid_to_date_error(response.errors.paid_to_date);
                        } else {
                            self.paid_to_date_error(null);
                        }

                        if (response.errors.invalid_date_range) {
                            self.messages.push(response.errors.invalid_date_range);
                        }


                    } else {
                        self.paid_from_date_error(null);
                        self.paid_to_date_error(null);
                        // self.invalid_date_range(null);

                        self.entry_rows([]);

                        var c = 0;
                        self.entry_rows(ko.utils.arrayMap(response.data, function (data) {

                            c += 1;

                            var row = ko.mapping.fromJS(data, {}, PaymentEntryRow());
                            if (typeof(row.row_errors) == 'undefined') {
                                row.row_errors = ko.observableArray([]);
                            }
                            if (c == 1) {
                                self.paid_from_date(row.paid_from_date());
                                self.paid_to_date(row.paid_to_date());
                            }
                            return row;
                        }));
                    }
                },
                error: function (errorThrown) {
                    self.messages.push(errorThrown);
                }
            });
    };

    // Set employee options
    self.update_employee_options = function () {
        $.ajax({
            url: '/payroll/get_employee_options/',
            method: 'POST',
            dataType: 'json',
            // async: true,
            data: {
                branch: self.branch() ? self.branch() : 'ALL'
            },
            success: function (response) {
                self.employee_options(response.opt_data);
                console.log('emplotee options loading success');
            },
            error: function (errorThrown) {
                console.log(errorThrown);
            }
        });
    };
    self.update_employee_options();
    self.branch.subscribe(function () {
        console.log('employee options updated');
        self.update_employee_options();
    });

    self.employee_options.subscribe(function(){
        var branch_emp_ids = ko.utils.arrayMap(self.employee_options(), function(obj){
            return parseInt(obj.id)
        });
        var rows_to_remove = []
        for (var roo of self.entry_rows()) {
            if($.inArray(roo.employee_id, branch_emp_ids) == -1){
                console.log('just removed one row');
                rows_to_remove.push(roo);
            }
        }
        self.entry_rows.removeAll(rows_to_remove);
    });

    self.selected_employees = ko.computed(function () {
        var sel_e = [];
        for (var row of self.entry_rows()) {
            if (typeof(row.paid_employee()) != 'undefined') {
                sel_e.push(row.paid_employee());
            }
        }
        return sel_e;
        // self.selected_employees(sel_e);
    });
    self.update_employees_options = ko.computed(function () {
        for (var roow of self.entry_rows()) {
            roow.emp_options(self.employee_options().slice());
            var to_remove = [];
            for (var opt of roow.emp_options()) {

                if ($.inArray(String(opt.id), self.selected_employees()) != -1 && String(opt.id) != roow.paid_employee()) {
                    to_remove.push(opt);
                }
            }
            var diff = $(roow.emp_options()).not(to_remove).get();
            // if(diff.length == 0){roow.emp_options([{'id': 0 , 'name': 'wrufesh'},]);}else{roow.emp_options(diff);}
            roow.emp_options(diff);
            // console.log(roow.emp_options())
        }
    });

    // self.entry_rows.subscribe();

    self.remove_alert = function (alert_msg) {
        self.messages.remove(alert_msg);
    };


}



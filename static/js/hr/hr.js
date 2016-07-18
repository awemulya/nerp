$(document).ready(function () {
    // ko.options.deferUpdates = true;
    vm = new PayrollEntry(ko_data.emp_options);
    ko.applyBindings(vm);
    if (ko_data.ctx_data) {
        var mapping = {
            'entry_rows': {
                create: function (options) {
                    var entry_row = ko.mapping.fromJS(options.data, {copy: ['is_explicitly_added_row']}, new PaymentEntryRow(ko_data.emp_options.slice(0)));
                    if (typeof(options.parent.paid_from_date()) == 'undefined') {
                        options.parent.paid_from_date(options.data.paid_from_date);
                        options.parent.paid_to_date(options.data.paid_to_date);
                    }
                    return entry_row
                }
            }
        };
        ko.mapping.fromJS(ko_data.ctx_data, mapping, vm);
    }
});

function diffByID(list1, list2, pdb) {
    if (list1.length >= list2.length) {
        var list1_ids = ko.utils.arrayMap(list1, function (obj) {
            return obj.id
        });
        var list2_ids = ko.utils.arrayMap(list2, function (obj) {
            return obj.id
        });
        var diff = $(list1_ids).not(list2_ids).get();

        var diff_obj_array = ko.utils.arrayFilter(list1, function (obj) {

            if ($.inArray(obj.id, diff) != -1) {
                return obj
            }
        });

        if (pdb) {
            debugger;
        }
        return diff_obj_array;
    }

}

function PaymentEntryRow(emp_options) {
    var self = this;
    self.id = ko.observable();
    self.emp_options = ko.observableArray(emp_options);
    // self.emp_options.extend({notify: 'always'});
    self.paid_employee = ko.observable();
    // self.employee_id = null;

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
    self.request_flag = ko.observable(false);
    self.row_errors = ko.observableArray();
    self.disable_input = ko.observable(false);


    self.incentive_details = ko.observableArray();
    self.allowance_details = ko.observableArray();
    self.deduction_details = ko.observableArray();

    self.deduction_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.deduction_details(), function (obj) {
            total += parseInt(obj.amount());
        });
        self.deduced_amount(total);
    });

    self.allowance_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.allowance_details(), function (obj) {
            total += parseInt(obj.amount());
        });
        self.allowance(total);
    });

    self.incentive_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.incentive_details(), function (obj) {
            total += parseInt(obj.amount());
        });
        self.incentive(total);
    });

    self.is_explicitly_added_row = true;

    self.process_request_flag = ko.computed(function () {
        if (self.paid_employee() && self.paid_from_date() && self.paid_to_date()) {
            self.request_flag(true);
        }

    });

    // self.emp_options.subscribe(function () {
    //     self.paid_employee(self.employee_id);
    // });
    // self.paid_employee.subscribe(function () {
    //     console.log('This is paid employee')
    //     console.log(self.paid_employee());
    //     // if (self.paid_employee()) {
    //     //     self.employee_id = parseInt(self.paid_employee());
    //     // }
    //     self.request_flag(true);
    // });

    // self.employee_changed = function () {
    //     // console.log('We entered here successfully');
    //     console.log(self.paid_employee());
    //     debugger;
    //     self.request_flag(true);
    //     // self.setOtrParam();
    //     // if (event.originalEvent) { //user changed
    //     // } else { // program changed
    // };

    // Make here a observable function dat will set other parameters with employee id and date range
    self.request_flag.subscribe(function () {
        if (self.request_flag() == true && vm.payroll_type() == "INDIVIDUAL" && self.is_explicitly_added_row) {
            $.ajax({
                url: '/payroll/get_employee_account/',
                method: 'POST',
                dataType: 'json',
                data: {
                    paid_employee: self.paid_employee(),
                    paid_from_date: self.paid_from_date(),
                    paid_to_date: self.paid_to_date(),
                    is_monthly_payroll: vm.is_monthly_payroll(),
                    edit: vm.id()
                },
                // async: true,
                success: function (response) {
                    if (response.errors) {
                        vm.entry_rows([new PaymentEntryRow()]);
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
                        ko.mapping.fromJS(response.data, mapping, self);

                        if (typeof(response.data.row_errors) == 'undefined') {
                            self.row_errors([]);
                        }
                        self.request_flag(false);

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
        // self.request_flag(false);
    });
}

function PayrollEntry(employee_options) {
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

    self.is_monthly_payroll = ko.observable(true);

    self.branch = ko.observable();

    self.messages = ko.observableArray();

    self.employee_options = ko.observableArray(employee_options);

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
        if (self.payroll_type() == 'INDIVIDUAL') {
            // debugger;
            if (!self.entry_rows().length) {
                self.entry_rows.push(new PaymentEntryRow(employee_options.slice(0)));
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
        self.entry_rows.push(new PaymentEntryRow(employee_options.slice(0)));
    };
    self.removeRow = function (row) {
        self.entry_rows.remove(row);
    };
    self.set_time_stamp = ko.computed(function () {
        // console.log('We are in timestamp function');
        if (self.payroll_type() != 'GROUP') {

            if (self.paid_from_date() && self.paid_to_date()) {
                for (var o of self.entry_rows()) {
                    o.paid_from_date(self.paid_from_date());
                    o.paid_to_date(self.paid_to_date());
                }
            }
        }
    });

    self.request_flag = ko.computed(function () {
        return self.branch() + self.paid_from_date() + self.paid_to_date();
    });

    self.getGroupSalary = function () {
    };

    self.request_flag.subscribe(function () {
        if (self.payroll_type() == 'GROUP' && self.paid_from_date() && self.paid_to_date()) {

            $.ajax({
                url: '/payroll/get_employees_account/',
                method: 'POST',
                dataType: 'json',
                data: {
                    branch: self.branch() ? self.branch() : 'ALL',
                    paid_from_date: self.paid_from_date(),
                    paid_to_date: self.paid_to_date(),
                    is_monthly_payroll: self.is_monthly_payroll(),
                    edit: self.id()
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

                        self.entry_rows([]);

                        var c = 0;
                        self.entry_rows(ko.utils.arrayMap(response.data, function (data) {

                            c += 1;
                            var mapping = {
                                'ignore': ["emp_options"]
                            };
                            var row = ko.mapping.fromJS(data, mapping, new PaymentEntryRow(employee_options.slice(0)));
                            // row.is_explicitly_added_row = false;
                            row.request_flag(false);
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
        }
    });

    // Set employee options
    self.update_employee_options = function () {
        $.ajax({
            url: '/payroll/get_employee_options/',
            method: 'POST',
            dataType: 'json',
            // async: false,
            data: {
                branch: self.branch() ? self.branch() : 'ALL'
            },
            success: function (response) {
                // self.employee_options(response.opt_data);


                // dont delete just trim emp_options (ie either push or pop)
                if (self.employee_options().length > response.opt_data.length) {
                    // debugger;
                    self.employee_options.removeAll(diffByID(self.employee_options(), response.opt_data));
                } else if (self.employee_options().length < response.opt_data.length) {
                    ko.utils.arrayPushAll(self.employee_options, diffByID(response.opt_data, self.employee_options()))
                } else {
                    // self.employee_options(response.opt_data);
                    self.employee_options.removeAll(diffByID(self.employee_options(), response.opt_data));
                    ko.utils.arrayPushAll(self.employee_options, diffByID(response.opt_data, self.employee_options()))
                }
                // self.employee_options(response.opt_data);

            },
            error: function (errorThrown) {
                console.log(errorThrown);
            }
        });
    };
    // self.update_employee_options();
    self.branch.subscribe(function () {
        self.update_employee_options();
    });

    self.employee_options.subscribe(function () {
        var branch_emp_ids = ko.utils.arrayMap(self.employee_options(), function (obj) {
            return obj.id
        });
        var rows_to_remove = [];
        for (var roo of self.entry_rows()) {
            if ($.inArray(roo.paid_employee(), branch_emp_ids) == -1) {
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
    });

    self.update_employees_options = ko.computed(function () {
        // debugger;
        for (var roow of self.entry_rows()) {

            // dont delete just trim emp_options (ie either push or pop)
            // if (self.employee_options().length > roow.emp_options().length) {
            //     // roow.emp_options.removeAll($(self.employee_options()).not(roow.emp_options()).get());
            //     ko.utils.arrayPushAll(roow.emp_options, diffByID(self.employee_options(), roow.emp_options()))
            // } else if (self.employee_options().length < roow.emp_options().length) {
            //     roow.emp_options.removeAll(diffByID(roow.emp_options(), self.employee_options()));
            // } else {
            //     roow.emp_options(self.employee_options().slice())
            // }
            roow.emp_options(self.employee_options().slice());

            var to_remove = [];
            for (var opt of roow.emp_options()) {

                if ($.inArray(opt.id, self.selected_employees()) != -1 && opt.id != roow.paid_employee()) {
                    to_remove.push(opt);
                }
            }

            // console.log('to remove diff')
            // console.log(roow.emp_options(), to_remove);
            // console.log(diffByID(roow.emp_options(), to_remove, true));

            // var diff = $(roow.emp_options()).not(to_remove).get();
            roow.emp_options(diffByID(roow.emp_options(), to_remove));

            // console.log(diff);
            // roow.emp_options.removeAll(diffByID(roow.emp_options(), to_remove));

            //  // dont delete just trim emp_options (ie either push or pop)
            // if(roow.emp_options().length > to_remove.length ){
            //    roow.emp_options.removeAll(to_remove);
            // }

            // // roow.paid_employee(roow.employee_id);
        }
    });

    self.remove_alert = function (alert_msg) {
        self.messages.remove(alert_msg);
    };
}



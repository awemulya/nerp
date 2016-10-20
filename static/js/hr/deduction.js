/**
 * Created by wrufesh on 10/20/16.
 */
var deduction = {
    getList: function (url, success_callback) {
        App.showProcessing();
        App.remoteGet(
            url,
            {},
            success_callback,
            function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            }
        );
    },
    postData: function (url, payload, callback) {
        App.showProcessing();
        App.remotePost(
            url,
            payload,
            callback,
            function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            }
        );

    },
    deductionVm: function (data, validity_id) {
        var self = this;
        self.id = ko.observable();
        self.name = ko.observable();
        self.deduct_type = ko.observable();
        self.value = ko.observable();
        self.description = ko.observable();
        self.priority = ko.observable();
        self.is_refundable_deduction = ko.observable();
        self.is_tax_free = ko.observable();
        self.is_optional = ko.observable();
        self.amount_editable = ko.observable();
        if (validity_id) {
            self.validity_id = ko.observable(validity_id)
        } else {
            self.validity_id = ko.observable()
        }
        if (data) {
            for (var k in data) {
                self[k](data[k]);
            }
        }

    },
    vm: function () {
        var self = this;
        App.validationSettings();

        // Grade scale Vality main observables
        self.validity_api_url = '/payroll/api/deduction-validity/';
        self.available_deduction_validities = ko.observableArray();
        self.selected_validity = ko.observable();
        // self.selected_validity.extend({required: true});
        // End Grade scale Vality main observables

        self.deductions = ko.observableArray();
        // Load deductions
        self.selected_validity.subscribe(function () {
            if (self.selected_validity()) {
                deduction.getList('/payroll/api/deduction/?validity_id=' + String(self.selected_validity().id()) + '/', function (res) {
                    if (res.length != 0) {
                        var vm_list = ko.utils.arrayMap(res, function (res_deduction) {
                                return new deduction.deductionVm(res, self.selected_validity().id())
                            }
                        );
                        self.deductions([]);
                        self.deductions(vm_list);
                    } else {
                        self.deductions.push(new deduction.deductionVm(null, self.selected_validity().id()))
                    }

                App.hideProcessing();
                });
            }
        });
        self.add_new = function () {
            self.deductions.push(new deduction.deductionVm(null, self.selected_validity().id()));
        };
        self.delete = function (row) {
            App.confirmAlert(
                'Are you sure you want to delete this deduction?',
                function () {
                    if(row.id()){
                        App.remoteDelete(
                        '/payroll/api/deduction/' + String(row.id()) + '/',
                        {},
                        function (res) {
                            App.notifyUser('Successfully Deleted', 'success');
                            self.deductions.remove(row);
                        },
                        function (err) {
                            var err_message = err.responseJSON.detail;
                            var error = App.notifyUser(
                                err_message,
                                'error'
                            );
                            App.hideProcessing();
                        }
                    )
                    }else{
                        self.deductions.remove(row);
                    }

                }
            );
        };

        self.save = function () {
            var payload = JSON.parse(ko.toJSON(self.deductions()));
            deduction.postData(
                '/payroll/api/deduction/',
                payload,
                function(){
                    App.notifyUser('Successfully Saved', 'success')
                }
            )
        };

        // End Load deductions
    }
};
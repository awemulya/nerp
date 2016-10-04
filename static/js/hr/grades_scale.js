/**
 * Created by wrufesh on 9/18/16.
 */
var gradeScale = {
        // TODO get gradeScaleValidity
        // TODO get employeeGrades
        // TODO get employeeGradeScales
        getGradeScaleValidities: function (success_callback) {
            App.showProcessing();
            App.remoteGet(
                '/payroll/api/grade-scale-validity/',
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

        addGradeScaleValidity: function () {

        },

        getParentGrades: function () {

        },

        getEmployeeGrades: function () {

        },

        validityVm: function (observableArray, data) {
            var self = this;
            self.id = ko.observable();

            self.valid_from = ko.observable();
            self.note = ko.observable();

            if(data){
                for(k in self){
                    self[k](data[k])
                }
            }

            self.list = observableArray;
            self.api_url = '/payroll/api/grade-scale-validity/';

            self.save = function () {
                App.showProcessing();
                App.remotePost(
                    self.api_url,
                    JSON.parse(ko.toJSON(self)),
                    function (res) {
                        console.log(res);
                        console.log('successfully saved');
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

            }
            self.update = function () {
                
            }

        },

        gradeScaleVm: function () {
            var self = this;
            self.id = ko.observable();
            self.grade_id = ko.observable();
            self.grade_name = ko.observable();
            self.parent_grade_id = ko.observable();
            // self.parent_grade_name = ko.observable();
            self.salary_scale = ko.observable();
            self.grade_number = ko.observable();
            self.grade_rate = ko.observable();
            self.validity_id = ko.observable();
        },

        vm: function () {
            var self = this;
            self.available_scale_validities = ko.observableArray();
            self.selected_validity = ko.observable();
            self.show_validity_modal = ko.observable(false);
            self.validity_modal_form = ko.observable(new gradeScale.validityVm(self.available_scale_validities));
            self.validity_add = function () {
                self.show_validity_modal(true);
                self.validity_modal_form(new gradeScale.validityVm(self.available_scale_validities));

            };
            self.validity_update = function () {
                self.show_validity_modal(true);
                self.validity_modal_form(self.selected_validity());
            }

            // Load grade scale
            gradeScale.getGradeScaleValidities(function(res) {
                var validities = ko.utils.arrayMap(res, function (item) {
                    return new gradeScale.validityVm(self.available_scale_validities, item);
                });
                self.available_scale_validities([]);
                self.available_scale_validities(validities);
                App.hideProcessing();
            });
            // End Load grade scale
        },
    }
    ;
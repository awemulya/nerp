/**
 * Created by wrufesh on 9/18/16.
 */

// TODO manage validity dates in bs
    
var gradeScale = {
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

            // End Grade scale Vality main observables
            var self = this;
            var validity_api_url = '/payroll/api/grade-scale-validity/';

            self.available_scale_validities = ko.observableArray();
            self.selected_validity = ko.observable();
            self.show_validity_modal = ko.observable(false);
            self.validity_modal_form = ko.observable(new validityVm(self.available_scale_validities, self.show_validity_modal, validity_api_url));

            self.validity_add = function () {
                self.show_validity_modal(true);
                self.validity_modal_form(new validityVm(self.available_scale_validities, self.show_validity_modal, validity_api_url));

            };
            self.validity_update = function () {
                self.validity_modal_form(self.selected_validity());
                self.show_validity_modal(true);
            };

            // Load grade scale
            gradeScale.getGradeScaleValidities(function (res) {
                var validities = ko.utils.arrayMap(res, function (item) {
                    return new validityVm(self.available_scale_validities, self.show_validity_modal, validity_api_url, item);
                });
                self.available_scale_validities([]);
                self.available_scale_validities(validities);
                App.hideProcessing();
            });
            // End Load grade scale
            
            // Grade scale Vality main observables
            
            
        },
    }
    ;
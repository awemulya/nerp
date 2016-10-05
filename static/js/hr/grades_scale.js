/**
 * Created by wrufesh on 9/18/16.
 */

// TODO manage validity dates in bs

var gradeScale = {


        addGradeScaleValidity: function () {

        },

        getParentGrades: function () {

        },

        getEmployeeGrades: function () {

        },
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
        gradeGroupVm: function(data){
            var self = this;
            self.id = ko.observable;
            self.name = ko.observable();
            self.employee_grades = ko.observableArray();

            // if (data) {
            //     for (var k in data) {
            //         self[k](data[k])
            //     }
            // }
        },

        gradeVm: function(data){
            var self = this;
            self.id = ko.observable();
            self.grade_name = ko.observable();
            self.grade_group_id = ko.observable();
            self.grade_scale = ko.observable();
            // if (data) {
            //     for (var k in data) {
            //         self[k](data[k])
            //     }
            // }
        },

        gradeScaleVm: function (data) {
            var self = this;
            self.id = ko.observable();
            self.grade_id = ko.observable();
            // self.grade_name = ko.observable();
            // self.parent_grade_id = ko.observable();
            // self.parent_grade_name = ko.observable();
            self.salary_scale = ko.observable();
            self.grade_number = ko.observable();
            self.grade_rate = ko.observable();
            self.validity_id = ko.observable();
            // if (data) {
            //     for (var k in data) {
            //         self[k](data[k])
            //     }
            // }
        }
        ,

        vm: function () {

            var self = this;
            // End Grade scale Vality main observables
            self.validity_api_url = '/payroll/api/grade-scale-validity/';
            self.available_scale_validities = ko.observableArray();
            self.selected_validity = ko.observable();
            // Grade scale Vality main observables

            self.available_grade_groups = ko.observableArray();
            gradeScale.getList(
                '/payroll/api/grade-group/',
                function (res) {
                    self.available_grade_groups(res)
                }
            );

            // self.grade_scales = ko.observableArray();
            // gradeScale.getList(
            //     '/payroll/api/grade-scale/',
            //     function (res) {
            //         var items = ko.utils.arrayMap(res, function (item) {
            //             return new gradeScale.gradeScaleVm(item);
            //         });
            //         self.grade_scales([]);
            //         self.grade_scales(items);
            //     }
            // );
            // self.grades = ko.observableArray();
            // gradeScale.getList(
            //     '/payroll/api/employee-grade.',
            //     function (res) {
            //         var items = ko.utils.arrayMap(res, function (item) {
            //             return new gradeScale.gradeVm(item);
            //         });
            //         self.grades([]);
            //         self.grades(items);
            //     }
            // );
        }
    }
    ;
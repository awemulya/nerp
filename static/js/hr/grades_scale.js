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
            self.validity_api_url = '/payroll/api/grade-scale-validity/';
            self.available_scale_validities = ko.observableArray();
            self.selected_validity = ko.observable();
            // Grade scale Vality main observables
        }
    }
    ;
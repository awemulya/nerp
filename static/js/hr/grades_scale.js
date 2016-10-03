/**
 * Created by wrufesh on 9/18/16.
 */
var gradeScale = {
    // TODO get gradeScaleValidity
    // TODO get employeeGrades
    // TODO get employeeGradeScales
    getGradeScaleValidities: function () {

    },

    addGradeScaleValidity: function () {

    },

    getParentGrades: function () {

    },

    getEmployeeGrades: function () {

    },

    gradeScaleVm: function () {
        var self = this;
        self.grade_id = ko.observable();
        self.grade_name = ko.observable();
        self.parent_grade_id = ko.observable();
        // self.parent_grade_name = ko.observable();
        self.salary_scale = ko.observable();
        self.grade_number = ko.observable();
        self.grade_rate = ko.observable();
        self.validity_id = ko.observable();
    },

    vm : function () {
        var self = this;
        self.available_scale_validites = ko.observableArray(['hello', 'hi']);
        self.selected_validity = ko.observable();
    },
}
;
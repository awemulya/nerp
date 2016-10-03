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

    validityVm: function () {
        var self = this;
        self.id = ko.observable();

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

    vm : function () {
        var self = this;
        self.available_scale_validities = ko.observableArray(['hello', 'hi']);
        self.selected_validity = ko.observable();
        self.show_validity_modal = ko.observable(false);
        self.validity_modal_form = ko.observable(new gradeScale.validityVm());
        self.validity_add = function () {
            self.show_validity_modal(true);
            self.validity_modal_form(new gradeScale.validityVm());

        };
        self.validity_update = function () {
            self.show_validity_modal(true);
            self.validity_modal_form(self.selected_validity());
        }
    },
}
;
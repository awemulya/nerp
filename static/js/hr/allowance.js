/**
 * Created by wrufesh on 10/17/16.
 */
/**
 * Created by wrufesh on 9/18/16.
 */

// TODO manage validity dates in bs

var allowance = {
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
        gradeScaleVm: function (grade_id, data, validity_id) {
            var self = this;
            self.id = ko.observable();
            if (grade_id) {
                self.grade_id = ko.observable(grade_id);
            } else {
                self.grade_id = ko.observable();
            }
            // self.grade_name = ko.observable();
            // self.parent_grade_id = ko.observable();
            // self.parent_grade_name = ko.observable();
            self.salary_scale = ko.observable();
            self.grade_number = ko.observable();
            self.grade_rate = ko.observable();
            if (validity_id) {
                self.validity_id = ko.observable(validity_id);
            } else {
                self.validity_id = ko.observable();
            }
            if (data) {
                for (var k in data) {
                    self[k](data[k])
                }
            }
        }
        ,

        vm: function () {

            var self = this;
            // Grade scale Vality main observables
            self.validity_api_url = '/payroll/api/allowance-validity/';
            self.available_allowance_validities = ko.observableArray();
            self.selected_validity = ko.observable();
            // End Grade scale Vality main observables

            // Grade scale Vality main observables
            self.allowance_name_api_url = '/payroll/api/allowance-name/';
            self.available_allowance_names = ko.observableArray();
            self.selected_allowance = ko.observable();
            // End Grade scale Vality main observables

            // self.available_grade_groups = ko.observableArray();
            // gradeScale.getList(
            //     '/payroll/api/grade-group/',
            //     function (res) {
            //         ko.utils.arrayForEach(res, function (grade_group) {
            //                 ko.utils.arrayForEach(grade_group.employee_grades, function (grade) {
            //                     grade['scale'] = ko.observable(new gradeScale.gradeScaleVm(grade.id));
            //                 });
            //                 grade_group['visibility'] = ko.observable(false);
            //
            //                 grade_group['toggle_visibility'] = function () {
            //                     if (grade_group['visibility']() == false) {
            //                         grade_group['visibility'](true);
            //                     } else {
            //                         grade_group['visibility'](false);
            //                     }
            //                 };
            //                 //
            //                 // grade_group['save'] = function () {
            //                 //     console.log('Saving updated Value');
            //                 //     // TODO check whether the validity is selected or not(it needs to be selected)
            //                 // };
            //
            //             }
            //         );
            //         self.available_grade_groups(res);
            //         App.hideProcessing();
            //     });
            //
            //
            // var manage_list_response = function (res) {
            //     // Here res is all entered grade scale
            //     ko.utils.arrayForEach(self.available_grade_groups(), function (grade_group) {
            //         ko.utils.arrayForEach(grade_group.employee_grades, function (grade) {
            //             // console.log(grade['scale']().grade_rate(), grade['scale']().grade_number(), grade['scale']().salary_scale());
            //             var grade_scale = ko.utils.arrayFirst(res, function (scale) {
            //                 if (scale.grade_id == grade.id) {
            //                     return scale
            //                 }
            //             });
            //             if (grade_scale) {
            //                 grade['scale'](new gradeScale.gradeScaleVm(grade.id, grade_scale, self.selected_validity().id()));
            //             } else {
            //                 grade['scale'](new gradeScale.gradeScaleVm(grade.id, null, self.selected_validity().id()));
            //             }
            //         });
            //     });
            //     App.hideProcessing();
            //     App.notifyUser('Success', 'success');
            // };

            self.selected_validity.subscribe(function () {
                // if (self.selected_validity()) {
                //     gradeScale.getList(
                //         '/payroll/api/grade-scale/?validity_id=' + String(self.selected_validity().id()),
                //         manage_list_response
                //     );
                // } else {
                //     ko.utils.arrayForEach(self.available_grade_groups(), function (grade_group) {
                //         ko.utils.arrayForEach(grade_group.employee_grades, function (grade) {
                //             grade['scale'](new gradeScale.gradeScaleVm(grade.id));
                //         });
                //
                //     });
                // }
            });

            // self.save_update = function () {
            //     if (self.selected_validity()) {
            //         var payload = JSON.parse(ko.toJSON(self.available_grade_groups()));
            //         gradeScale.postData(
            //             '/payroll/api/grade-scale/?validity_id=' + String(self.selected_validity().id()),
            //             payload,
            //             manage_list_response
            //         )
            //     }
            // };

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
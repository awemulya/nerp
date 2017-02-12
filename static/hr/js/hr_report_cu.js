$(document).ready(function () {
    vm = new ReportHR(ko_data.obj_id);
    ko.applyBindings(vm);
    // if (ko_data.ctx_data) {
    //     var mapping = {
    //         'entry_rows': {
    //             create: function (options) {
    //                 var entry_row = ko.mapping.fromJS(options.data, {copy: []}, new PaymentEntryRow(ko_data.emp_options.slice(0)));
    //                 // if (typeof(options.parent.paid_from_date_input()) == 'undefined') {
    //                 //     options.parent.paid_from_date_input(options.data.paid_from_date);
    //                 //     options.parent.paid_to_date_input(options.data.paid_to_date);
    //                 // }
    //                 return entry_row;
    //             }
    //         },
    //         // 'branch': {
    //         //     create: function(options){
    //         //         console.log(options.data)
    //         //         if(options.data == null){
    //         //             return 'ALL'
    //         //         }
    //         //         return options.data
    //         //     }
    //         // }
    //     };
    //     ko.mapping.fromJS(ko_data.ctx_data, mapping, vm);

    // }
});

function ReportTableDetail(){
    var self = this;
    self.id = ko.observable();
    self.field_name = ko.observable();
    self.field_description = ko.observable();
    self.order = ko.observable();
    self.need_total = ko.observable();
}

function ReportTable(obj_id){
    var self = this;
    self.id = ko.observable();
    self.title = ko.observable();
    self.table_details = ko.observableArray();
    if (!obj_id){
        self.table_details.push(new ReportTableDetail());
    }

    self.add_new_field = function(){
        self.table_details.push(new ReportTableDetail());   
    };
}


function ReportHR(obj_id){
    var self = this;
    self.id = ko.observable();
    self.name = ko.observable();
    self.code = ko.observable();
    self.template = ko.observable();
    self.for_employee_type = ko.observable();
    self.report_tables = ko.observableArray();
    if (!obj_id){
        self.report_tables.push(new ReportTable(obj_id));
    }

    self.add_new_table = function(){
        self.report_tables.push(new ReportTable(obj_id));
    };
}
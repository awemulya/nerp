$(document).ready(function () {
    vm = new BudgetAllocationItem(ko_data);
    ko.applyBindings(vm);
});

function BudgetAllocationItem(data) {
    var self = this;
    self.budget_head = ko.observableArray(data.budget_head);

    self.aids = ko.observableArray();

    self.count = []


    for (var k in data.rows) {
        if (data.rows[k].aid_name != null) {
            if (self.count.indexOf(data.rows[k].aid_name) == -1) {
                self.count.push(data.rows[k].aid_name);
                self.aids.push(data.rows[k].aid_name.split('-')[1]);
            }
        }
    }
    ;

    self.table_view = new TableViewModel({rows: data.rows, argument: self, auto_add_first: false}, RowVM);
    self.save = function () {

    };
};

function RowVM(row, vm) {
    var self = this;
    self.budget_head_id = ko.observable();
    self.goa_amount = ko.observable();

    if (row.aid_name == null) {
        self.goa_amount(row.amount)
    };

    for (i in vm.count) {
        self[vm.count[i]] = ko.observable();
        if (row.aid_name == vm.count[i]) {
            self[vm.count[i]](row.amount)
        }
    }

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }


}

$(document).ready(function () {
    vm = new BudgetAllocationItem(ko_data);
    ko.applyBindings(vm);
});

function BudgetAllocationItem(data) {
    var self = this;
    self.budget_head = ko.observableArray(data.budget_head);

    self.aids = ko.observableArray();

    self.count = []

    for (var k in data.aid) {
        if (data.aid[k].aid_name != null) {
            if (self.count.indexOf(data.aid[k].aid_name) == -1) {
                self.count.push(data.aid[k].aid_name);
                self.aids.push(data.aid[k].aid_name.split('-')[1]);
            }
        }
    }
    ;


    self.values = []
    self.value_count = []
    for (var i in data.rows) {
        var val = data.rows[i].budget_head_id
        if (self.value_count.indexOf(val) == -1) {
            self.value_count.push(val);
            self.values.push({
                'budget_head_id': val,
                'aid_amount': [{'aid_name': data.rows[i].aid_name, 'amount': data.rows[i].amount}],
            });

        } else  {
            var obj = $.grep(self.values, function(e){
                return e.budget_head_id == data.rows[i].budget_head_id;
            });
            obj[0].aid_amount.push({'aid_name': data.rows[i].aid_name, 'amount': data.rows[i].amount})
        }
    }

    self.table_view = new TableViewModel({rows: self.values, argument: self, auto_add_first: false}, RowVM);
    self.save = function () {

    };
};

function RowVM(row, vm) {
    var self = this;
    self.budget_head_id = ko.observable();
    self.goa_amount = ko.observable();

    if (row) {
        //if (row.aid_name == null) {
        //    self.goa_amount(row.amount)
        //}
        //;

        for (i in vm.count) {
            self[vm.count[i]] = ko.observable();
            if (row.aid_name == vm.count[i]) {
                self[vm.count[i]](row.amount)
            }
        }
        for (i in row.aid_amount) {
            if (row.aid_amount[i].aid_name == null){
                if (self.goa_amount() == undefined) {
                    self.goa_amount(row.aid_amount[i].amount);
                } else {
                    debugger
                    self.goa_amount(self.goa_amount() + row.aid_amount[i].amount)
                }
            }
            if (row.aid_amount[i].aid_name == vm.count[i]) {
                self[vm.count[i]](row.aid_amount[i].amount)
            }
        }
    }

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }


}

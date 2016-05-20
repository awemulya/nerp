$(document).ready(function () {
    vm = new Expenditure(ko_data);
    ko.applyBindings(vm);
});

function Expenditure(data) {
    var self = this;
    self.budget_head = ko.observableArray(data.budget_head);

    self.aids = ko.observableArray();

    self.count = []

    self.fy = ko.observable(data.fy);
    self.project_id = ko.observable(data.project_id);

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
                'aid_amount': [{
                    'id': data.rows[i].id,
                    'aid_name': data.rows[i].aid_name,
                    'amount': data.rows[i].amount
                }],
            });

        } else {
            var obj = $.grep(self.values, function (e) {
                return e.budget_head_id == data.rows[i].budget_head_id;
            });
            obj[0].aid_amount.push({
                'id': data.rows[i].id,
                'aid_name': data.rows[i].aid_name,
                'amount': data.rows[i].amount
            });
        }
    }

    self.table_view = new TableViewModel({rows: self.values, argument: self}, RowVM);

    self.save = function () {
        $.ajax({
            type: "POST",
            url: '/project/expenditure/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');

                    for (var i in msg.rows) {
                        for (var aid in msg.rows[i]) {
                            self.table_view.rows()[i][aid](msg.rows[i][aid]);
                            if (self.table_view.rows()[i].aid_amount().length == 0) {
                                self.table_view.rows()[i].aid_amount.push({'id': msg.rows[i][aid]});
                            }
                                }
                        }
                        self.table_view.deleted_rows([]);
                    }
                }
                ,
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    alert.error(textStatus.toTitleCase() + ' - ' + errorThrown);
                }
            });
    }
}

function RowVM(row, vm) {
    var self = this;
    self.id = ko.observable();
    self.budget_head_id = ko.observable();
    self.goa_amount = ko.observable();
    self.goa_id = ko.observable();
    self.aid_amount = ko.observableArray();

    for (i in vm.count) {
        self[vm.count[i]] = ko.observable();
        self[vm.count[i] + "-id"] = ko.observable();
    }

    if (row) {
        for (i in row.aid_amount) {
            if (row.aid_amount[i].aid_name == null) {
                if (self.goa_amount() == undefined) {
                    self.goa_amount(row.aid_amount[i].amount);
                    self.goa_id(row.aid_amount[i].id);
                } else {
                    self.goa_amount(self.goa_amount() + row.aid_amount[i].amount);
                }
            }
            if (self[row.aid_amount[i].aid_name] != undefined) {
                self[row.aid_amount[i].aid_name](row.aid_amount[i].amount);
                self[row.aid_amount[i].aid_name + "-id"](row.aid_amount[i].id);

            }
        }
    }

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.total = function () {
        var total = 0;
        if (self.goa_amount()) {
            total = parseInt(self.goa_amount());
        }
        for (i in vm.count) {
            if (typeof(self[vm.count[i]]()) != 'undefined') {
                if (self[vm.count[i]]() != null) {
                    total = total + empty_to_zero(self[vm.count[i]]());
                }
            }
        }
        return parseInt(total);
    }
}

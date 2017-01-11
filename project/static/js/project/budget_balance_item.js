$(document).ready(function () {
    vm = new BudgetBalance(ko_data);
    ko.applyBindings(vm);
    var total_col = $(".total").prev().children().length;
    $(".total td:first").first().attr('colspan', total_col - 2);
});

function BudgetBalance(data) {
    var self = this;
    self.budget_heads = ko.observableArray([]);
    self.capital_expenditure = ko.observableArray([]);


    ko.utils.arrayForEach(data.budget_heads, function (obj) {
        if (obj.recurrent) {
            self.budget_heads.push(obj);
        } else {
            self.capital_expenditure.push(obj);
        }
    });

    self.aids = ko.observableArray();

    self.count = [];

    //self.fy = ko.observable(data.fy);
    //self.project_id = ko.observable(data.project_id);
    self.project_fy_id = ko.observable(data.project_fy_id);

    for (var k in data.aids) {
        if (data.aids[k].aid_name != null) {
            if (self.count.indexOf(data.aids[k].aid_name) == -1) {
                self.count.push(data.aids[k].aid_name);
                self.aids.push(data.aids[k].aid_name.split('-')[1]);
            }
        }
    }


    self.budget_release_recurrent_values = [];
    self.budget_release_capital_expenditure_values = [];
    self.budget_release_value_count = [];

    for (var i = 0; i < data.budget_release.length; i++) {
        var val = data.budget_release[i].budget_head_id;
        if (data.budget_release[i].recurrent) {
            self.values = self.budget_release_recurrent_values;
        } else {
            self.values = self.budget_release_capital_expenditure_values;
        }
        if (self.budget_release_value_count.indexOf(val) == -1) {
            self.budget_release_value_count.push(val);
            self.values.push({
                'budget_head_id': val,
                'aid_amount': [{
                    'id': data.budget_release[i].id,
                    'aid_name': data.budget_release[i].aid_name,
                    'amount': data.budget_release[i].amount
                }]
            });

        } else {
            var obj = $.grep(self.values, function (e) {
                return e.budget_head_id == data.budget_release[i].budget_head_id;
            });
            obj[0].aid_amount.push({
                'id': data.budget_release[i].id,
                'aid_name': data.budget_release[i].aid_name,
                'amount': data.budget_release[i].amount
            });
        }
    }

    self.expenditure_recurrent_values = [];
    self.expenditure_capital_expenditure_values = [];
    self.expenditure_value_count = [];

    for (var i = 0; i < data.expenditure.length; i++) {
        var val = data.expenditure[i].budget_head_id;
        if (data.expenditure[i].recurrent) {
            self.values = self.expenditure_recurrent_values;
        } else {
            self.values = self.expenditure_capital_expenditure_values;
        }
        if (self.expenditure_value_count.indexOf(val) == -1) {
            self.expenditure_value_count.push(val);
            self.values.push({
                'budget_head_id': val,
                'aid_amount': [{
                    'id': data.expenditure[i].id,
                    'aid_name': data.expenditure[i].aid_name,
                    'amount': data.expenditure[i].amount
                }]
            });

        } else {
            var obj = $.grep(self.values, function (e) {
                return e.budget_head_id == data.expenditure[i].budget_head_id;
            });
            obj[0].aid_amount.push({
                'id': data.expenditure[i].id,
                'aid_name': data.expenditure[i].aid_name,
                'amount': data.expenditure[i].amount
            });
        }
    }

    self.budget_balance_recurrent_values = [];
    self.budget_balance_expenditure_values = [];
    for (var i = 0; i < self.budget_heads().length; i++) {

        var budget_release_obj = $.grep(self.budget_release_recurrent_values, function (e) {
            return e.budget_head_id == self.budget_heads()[i].id;
        })[0];
        var expenditure_obj = $.grep(self.expenditure_recurrent_values, function (e) {
            return e.budget_head_id == self.budget_heads()[i].id;
        })[0];

        if (budget_release_obj) {
            var obj = {};
            obj['budget_head_id'] = self.budget_heads()[i].id;
            obj['budget_release'] = budget_release_obj;
            if (expenditure_obj)
                obj['expenditure'] = expenditure_obj;
            self.budget_balance_recurrent_values.push(obj);
        }
    }

    for (var i = 0; i < self.capital_expenditure().length; i++) {
        var budget_release_obj = $.grep(self.budget_release_capital_expenditure_values, function (e) {
            return e.budget_head_id == self.capital_expenditure()[i].id;
        })[0];
        var expenditure_obj = $.grep(self.expenditure_capital_expenditure_values, function (e) {
            return e.budget_head_id == self.capital_expenditure()[i].id;
        })[0];
        if (budget_release_obj) {
            var obj = {};
            obj['budget_head_id'] = self.capital_expenditure()[i].id;
            obj['budget_release'] = budget_release_obj;
            if (expenditure_obj)
                obj['expenditure'] = expenditure_obj;
            self.budget_balance_expenditure_values.push(obj);
        }
    }
    //console.log(self.expenditure_capital_expenditure_values);

    self.budget_head_view = new TableViewModel({rows: self.budget_balance_recurrent_values, argument: self}, RowVM);
    self.capital_expenditure_view = new TableViewModel({
        rows: self.budget_balance_expenditure_values,
        argument: self
    }, RowVM);

    self.budget_head_goa_sub_total = function () {
        var sum = 0;
        self.budget_head_view.rows().forEach(function (budget_head) {
            if (budget_head.goa_amount()) {
                sum += parseFloat(budget_head.goa_amount());
            }
        });
        return round2(sum);
    };

    self.budget_head_sub_total = function () {
        var sum = 0;
        self.budget_head_view.rows().forEach(function (budget_head) {
            if (budget_head.total()) {
                sum += parseFloat(budget_head.total());
            }
        });
        return round2(sum);
    };

    for (var index = 0; index < self.count.length; index++) {
        var name = self.count[index];
        self['budget-head-' + self.count[index] + '-sub-total'] = function (name) {
            var sum = 0;
            self.budget_head_view.rows().forEach(function (budget_head) {
                if (budget_head[name]()) {
                    sum += parseFloat(budget_head[name]());
                }
            });
            return round2(sum);
        };
    }

    self.capital_expenditure_sub_total = function () {
        var sum = 0;
        self.capital_expenditure_view.rows().forEach(function (capital_expenditure) {
            if (capital_expenditure.total()) {
                sum += parseFloat(capital_expenditure.total());
            }
        });
        return round2(sum);
    };

    for (var index = 0; index < self.count.length; index++) {
        var name = self.count[index];
        self['capital-expenditure-' + self.count[index] + '-sub-total'] = function (name) {
            var sum = 0;
            self.capital_expenditure_view.rows().forEach(function (capital_expenditure) {
                if (capital_expenditure[name]()) {
                    sum += parseFloat(capital_expenditure[name]());
                }
            });
            return round2(sum);
        };
    }

    self.capital_expenditure_goa_sub_total = function () {
        var sum = 0;
        self.capital_expenditure_view.rows().forEach(function (capital_expenditure) {
            if (capital_expenditure.goa_amount()) {
                sum += parseFloat(capital_expenditure.goa_amount());
            }
        });
        return round2(sum);
    };

    self.grand_total = function () {
        var total = 0;
        self.budget_head_view.rows().forEach(function (i) {
            total = total + i.total();
        });

        self.capital_expenditure_view.rows().forEach(function (i) {
            total += i.total();
        });
        return total;
    };

    self.save = function () {
        $.ajax({
            type: "POST",
            url: '/project/budget_release/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');
                    $("#tbody > tr").each(function (i) {
                        $($("#tbody > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows.budget_head_view) {
                        for (var aid in msg.rows.budget_head_view[i]) {
                            self.budget_head_view.rows()[i][aid](msg.rows.budget_head_view[i][aid]);
                            if (self.budget_head_view.rows()[i].aid_amount().length != 0) {
                                self.budget_head_view.rows()[i].aid_amount().push({'id': msg.rows.budget_head_view[i][aid]});
                            }
                        }
                    }
                    for (var i in msg.rows.capital_expenditure_view) {
                        for (var aid in msg.rows.capital_expenditure_view[i]) {
                            self.capital_expenditure_view.rows()[i][aid](msg.rows.capital_expenditure_view[i][aid]);
                            if (self.capital_expenditure_view.rows()[i].aid_amount().length != 0) {
                                self.capital_expenditure_view.rows()[i].aid_amount().push({'id': msg.rows.capital_expenditure_view[i][aid]});
                            }
                        }
                    }
                    self.budget_head_view.deleted_rows([]);
                    self.capital_expenditure_view.deleted_rows([]);
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
    self.budget_head = ko.observable();

    for (i in vm.count) {
        self[vm.count[i]] = ko.observable();
        self[vm.count[i] + "-id"] = ko.observable();
    }


    if (row) {
        for (i in row.budget_release.aid_amount) {
            var expenditure_amount = 0;
            if ('expenditure' in row) {
                var expenditure_obj = $.grep(row.expenditure.aid_amount, function (e) {
                    return e.aid_name == row.budget_release.aid_amount[i].aid_name;
                })[0];

                if (expenditure_obj)
                    expenditure_amount = expenditure_obj.amount;
            }
            if (row.budget_release.aid_amount[i].aid_name === null) {
                if (self.goa_amount() == undefined) {
                    self.goa_amount(row.budget_release.aid_amount[i].amount - expenditure_amount);
                    self.goa_id(row.budget_release.aid_amount[i].id);
                }
                //else {
                //    self.goa_amount(self.goa_amount() + row.budget_release.aid_amount[i].amount);
                //}
            }
            if (self[row.budget_release.aid_amount[i].aid_name] != undefined) {
                self[row.budget_release.aid_amount[i].aid_name](row.budget_release.aid_amount[i].amount - expenditure_amount);
                self[row.budget_release.aid_amount[i].aid_name + "-id"](row.budget_release.aid_amount[i].id);

            }
        }
    }
    //debugger;
    if (row) {
        for (var k in row.budget_release) {
            self[k] = ko.observable(row.budget_release[k]);
        }
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

$(document).ready(function () {
    vm = new InventoryAccountVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function InventoryAccountVM(data) {

    var self = this;

    self.get_rows = function () {
        return self.table_vm.rows();
    }

    self.table_vm = new TableViewModel({rows: data, auto_add_first: false, argument: self.get_rows}, InventoryAccountRow);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/account/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert.error(textStatus);
            }
        });
    }

}

function InventoryAccountRow(data, get_all_rows) {

    var self = this;

    for (var i in data) {
        self[i] = ko.observable(data[i]);
    }

    if (self.income_quantity()) {
        self.expense_total(null);
    }

    self.wrapper = ko.observable(0);

    self.wrapper.remaining_total = function (root, index) {
        return ko.computed({
            read: function () {
                var root_vm = root;
                if (self.remaining_total_cost_price()) {
                    return self.remaining_total_cost_price();
                }
                if (index() == 0) {
                    ret = r2z(self.income_total()) - r2z(self.expense_total());
                } else {
                    ret = root_vm.table_vm.rows()[index() - 1].remaining_total_cost_price() + r2z(self.income_total()) - r2z(self.expense_total());

                }
                self.remaining_total_cost_price(ret);
                return ret;
            },
            write: function (value) {
                self.remaining_total_cost_price(value);
            },
        }, self);
    }.bind(self.flags);
}
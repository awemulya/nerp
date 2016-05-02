$(document).ready(function () {
    vm = new ImprestVM(ko_data);
    ko.applyBindings(vm);
});


function ImprestVM(data) {
    var self = this;

    self.table_view = new TableViewModel({rows: data, argument: self}, ImprestTransaction);

    self.add_transaction = function (transaction_data) {
        if (!transaction_data['name']) {
            transaction_data['name'] = transaction_data['type'].toTitleCase();
        }
        var initial_deposit = new ImprestTransaction(transaction_data);
        self.table_view.rows.push(initial_deposit);
        // Add focus to name of new row
        $('table.imprest-ledger tr').eq(2 + self.table_view.rows().length).find('.name').focus();
    }

    self.add_initial_deposit = function () {
        if (self.count_transaction_types('initial_deposit')()) {
            alert.error('There can only be one initial deposit!');
            return false;
        }
        self.add_transaction({'type': 'initial_deposit'});
    }

    self.add_replenishment_received = function () {
        self.add_transaction({'type': 'replenishment_received'});
    }

    self.add_gon_fund_transfer = function () {
        self.add_transaction({'type': 'gon_fund_transfer', 'name': 'Ka-7-15 Transfer'});
    }

    self.add_payment = function () {
        self.add_transaction({'type': 'payment'});
    }

    self.add_liquidation = function () {
        self.add_transaction({'type': 'liquidation'});
    }

    self.count_transaction_types = function (type) {
        return ko.computed(function () {
            var transactions = ko.utils.arrayFilter(vm.table_view.rows(), function (row) {
                return row.type() == type;
            });
            return transactions.length;
        })
    }

    self.sort = function () {
        // Sort ascending by date
        self.table_view.rows.sort(function (l, r) {
            var l_date = new Date(l.date());
            var r_date = new Date(r.date());
            return l_date.getTime() > r_date.getTime();
        });

        // Always keep initial_deposit on top
        self.table_view.rows.sort(function (l, r) {
            return r.type() == 'initial_deposit';
        });
    }

    self.sort();

    self.save = function () {
        self.sort();
        var initial_deposits = self.count_transaction_types('initial_deposit')();
        if (initial_deposits < 1) {
            alert.error('Initial Deposit is required!');
            return false;
        } else if (initial_deposits > 1) {
            alert.error('There can only be one initial deposit!');
            return false;
        }
        //$.ajax({
        //    type: "POST",
        //    url: '/inventory/save/demand_forms/',
        //    data: ko.toJSON(self),
        //    success: function (msg) {
        //        if (typeof (msg.error_message) != 'undefined') {
        //            alert.error(msg.error_message);
        //        }
        //        else {
        //            alert.success('Saved!');
        //            self.status('Requested');
        //            if (msg.id)
        //                self.id(msg.id);
        //            $("#tbody > tr").each(function (i) {
        //                $($("#tbody > tr")[i]).addClass('invalid-row');
        //            });
        //            for (var i in msg.rows) {
        //                self.table_view.rows()[i].id = msg.rows[i];
        //                $($("#tbody > tr")[i]).removeClass('invalid-row');
        //            }
        //        }
        //    },
        //    error: function (XMLHttpRequest, textStatus, errorThrown) {
        //        alert.error(textStatus.toTitleCase() + ' - ' + errorThrown);
        //    }
        //});
    }
}

function ImprestTransaction(row, imprest_vm) {
    var self = this;
    self.name = ko.observable();
    self.wa_no = ko.observable();
    self.ref = ko.observable();
    self.date = ko.observable();
    self.description = ko.observable();
    self.exchange_rate = ko.observable();
    self.type = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.entry_type = function () {
        if ($.inArray(self.type(), ['initial_deposit', 'replenishment_received']) != -1) {
            return 'dr';
        } else {
            return 'cr';
        }
    }
}
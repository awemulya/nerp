$(document).ready(function () {
    vm = new StockEntryViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function StockEntryViewModel(data) {

    var self = this;

    for (var k in data)
        self[k] = ko.observable(data[k]);

    initial_account_no = self.inventory_existing_account_no();

    self.existing_account_no = ko.observableArray(initial_account_no);
    self.new_account_no = ko.observableArray([]);
    self.table_view = new TableViewModel({rows: data.rows, argument: self}, StockEntryRow);

    self.id.subscribe(function (id) {
        history.pushState(id, id, window.location.href + id + '/');
    });

    self.table_view.rows.subscribe(function (changes) {
        if (changes[0].status == 'deleted') {
            var account_no = changes[0].value.account_no();
            var index = vm.existing_account_no().indexOf(account_no)
            vm.existing_account_no().splice(index, 1);
        }
    }, null, 'arrayChange');

    self.save = function (item, event) {
        var diff = $(self.existing_account_no()).not(self.new_account_no()).get();
        $.ajax({
            type: "POST",
            url: '/inventory/save/stock_entry/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    alert.success('Saved!');
                    if (msg.id)
                        self.id(msg.id);
                    $("#tbody > tr").each(function (i) {
                        $($("#tbody > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("#tbody > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
        });
    }
}


function StockEntryRow(row, stock_entry_vm) {

    var self = this;
    self.description = ko.observable();
    self.unit = ko.observable();
    self.opening_stock = ko.observable();
    self.account_no = ko.observable();
    self.opening_rate_vattable = ko.observable(false);
    self.opening_rate = ko.observable();
    self.name = ko.observable();

    var max_of_array = Math.max.apply(Math, stock_entry_vm.existing_account_no());

    for (var k in row)
        self[k] = ko.observable(row[k]);

    if (typeof(self.account_no()) == 'undefined') {
        self.account_no(max_of_array + 1 );
        stock_entry_vm.existing_account_no.push(max_of_array + 1);
        stock_entry_vm.new_account_no.push(max_of_array + 1);
    };


    self.account_no.subscribeChanged(function (newValue, oldValue) {
        var index = vm.existing_account_no().indexOf(oldValue);
        if (newValue == '') {
            newValue = 0;
        };
        vm.new_account_no.push(parseInt(newValue));
        vm.existing_account_no().splice(index, 1);
        vm.existing_account_no.push(parseInt(newValue));
    });

}
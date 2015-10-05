$(document).ready(function () {
    vm = new HandoverVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function HandoverVM(data) {

    var self = this;

    $.ajax({
        url: '/inventory/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data);
        }
    });

    self.msg = ko.observable('');
    self.status = ko.observable('standby');

    self.item_changed = function (row) {
        var selected_item = $.grep(self.items(), function (i) {
            return i.id == row.item_id();
        })[0];
        if (!selected_item) return;
        if (!row.specification())
            row.specification(selected_item.description);
        if (!row.unit())
            row.unit(selected_item.unit);
        row.inventory_classification_reference_no(selected_item.property_classification_reference_number);
        row.account_no(selected_item.account_no);
    }

    self.table_view = new TableViewModel({rows: data.rows}, HandoverRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        if (!self.voucher_no()) {
            alert.error('Voucher No. is required!');
            return false;
        }
        $.ajax({
            type: "POST",
            url: '/inventory/save/handover/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
//                    $('#message').html(msg.error_message);
//                    self.msg();
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
//            error: function(XMLHttpRequest, textStatus, errorThrown) {
//                $('#message').html(XMLHttpRequest.responseText.message);
//            }
        });
    }
}

function HandoverRow(row) {

    var self = this;
    self.account_no = ko.observable();
    self.inventory_classification_reference_no = ko.observable();
    self.item_id = ko.observable();
    self.specification = ko.observable();
    self.quantity = ko.observable().extend({ required: true });
    self.unit = ko.observable();
    self.total_amount = ko.observable();
    self.received_date = ko.observable();
    self.condition = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}
$(document).ready(function () {
    vm = new EntryReportVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function EntryReportVM(data) {

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


    self.table_view = new TableViewModel({rows: data.rows}, EntryReportRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/entry_report/',
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

function EntryReportRow(row) {

    var self = this;
    self.account_no = ko.observable();
    self.inventory_classification_reference_no = ko.observable();
    self.item_id = ko.observable();
    self.vattable = ko.observable(true);
    self.specification = ko.observable();
    self.quantity = ko.observable().extend({ required: true });
    self.unit = ko.observable();
    self.rate = ko.observable();
    self.remarks = ko.observable();
    self.other_expenses = ko.observable(0);



    self.amount = function () {
        return round2(parseFloat(self.rate()) + parseFloat(self.vat_amount()));
    }

    self.total = function () {
        return round2(self.amount() * parseFloat(self.quantity()) + empty_to_zero(self.other_expenses()));
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

    self.vat_amount = function () {
        var vat_rate;
        if (self.vattable()){
            vat_rate = 0.13;
        }else{
            vat_rate = 0;
        }
        return round2(self.rate() * vat_rate);
    }
}
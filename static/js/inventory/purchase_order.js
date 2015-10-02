$(document).ready(function () {
    vm = new PurchaseOrderViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function PurchaseOrderViewModel(data) {

    var self = this;

    $.ajax({
        url: '/inventory/items.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/parties.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.parties = ko.observableArray(data);
        }
    });

    self.party_name = ko.observable();
    self.party_address = ko.observable();
    self.party_pan_no = ko.observable();

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
    }

    self.sub_total = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            sum += i.total_amount();
        });
        return round2(sum);
    }

    self.vat_amount = function () {
        var sum = 0;
        self.table_view.rows().forEach(function (i) {
            if (i.vattable())
                sum += 0.13 * i.total_amount();
        });
        return round2(sum);
    }

    self.grand_total = function () {
        return self.sub_total() + self.vat_amount();
    }

    self.party_changed = function (obj) {
        if (typeof(obj.party()) == 'undefined')
            return false;
        var selected_obj = $.grep(self.parties(), function (i) {
            return i.id == obj.party();
        })[0];
        if (!selected_obj) return;
        obj.party_address(selected_obj.address);
        obj.party_name(selected_obj.name);
        obj.party_pan_no(selected_obj.pan_no);
    }

    self.table_view = new TableViewModel({rows: data.rows}, PurchaseRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.id.subscribe(function (id) {
        history.pushState(id, id, window.location.href + id + '/');
    });

    self.save = function (item, event) {
        if (!self.party()) {
            alert.error('Party is required!');
            return false;
        }
        $.ajax({
            type: "POST",
            url: '/inventory/save/purchase_order/',
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

function PurchaseRow(row) {

    var self = this;
    self.budget_title_no = ko.observable();
    self.item_id = ko.observable();
    self.specification = ko.observable();
    self.quantity = ko.observable().extend({ required: true });
    self.unit = ko.observable();
    self.rate = ko.observable();
    self.remarks = ko.observable();
    self.vattable = ko.observable(true);

    self.total_amount = function () {
        return round2(self.rate() * self.quantity());
    }

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
}
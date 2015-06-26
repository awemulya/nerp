$(document).ready(function () {
    vm = new DemandViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function DemandViewModel(data) {

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
        url: '/inventory/items_locations.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.items_locations = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/inventory/item_instances.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            //console.log(data);
            self.item_instances = ko.observableArray(data);
        }
    });

    self.msg = ko.observable('');
    self.status = ko.observable('standby');

    self.item_changed = function (row) {
        var selected_item = $.grep(self.items(), function (i) {
            return i.id == row.item_id();
        })[0];
        if (!selected_item) return;
        row.specification(selected_item.description);
        row.unit(selected_item.unit);
        row.inventory_account_id(selected_item.account_no);
    }

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, DemandRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/demand_form/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');
                    self.status('Requested');
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

function DemandRow(row, demand_vm) {

    var self = this;
    //default values
    self.item_id = ko.observable();
    self.specification = ko.observable();
    self.quantity = ko.observable().extend({required: true});
    self.unit = ko.observable();
    self.release_quantity = ko.observable();
    self.inventory_account_id = ko.observable();
    self.remarks = ko.observable();
    self.status = ko.observable('Requested');
    self.item = ko.observable();
    self.location = ko.observable();
    self.purpose = ko.observable();
    self.item_instances = ko.observableArray();


    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

    self.approve = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/approve/demand_form/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Approved!')
                    self.status('Approved');
                }
            }
        });
    }

    self.disapprove = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/disapprove/demand_form/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Disapproved!');
                    self.status('Requested');
                }
            }
        });
    }

    self.fulfill = function (root, item, event) {
        if (root.release_no() == '' || !root.release_no()) {
            alert.error('Release No. is required!');
            return false;
        }
        root.save();
        $.ajax({
            type: "POST",
            url: '/inventory/fulfill/demand_form/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Set as Fulfilled!')
                    self.status('Fulfilled');
                }
            }
        });
    }

    self.unfulfill = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/unfulfill/demand_form/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Set as Unfulfilled!');
                    self.status('Approved');

                }
            }
        });
    }

    self.release_focused = function (row, e) {
        $(e.currentTarget).click();
    }

    self.item_id.subscribe(function (val) {
        self.item_instances(get_by_id(demand_vm.item_instances, val));
    })

}
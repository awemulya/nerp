$(document).ready(function () {
    vm = new DemandViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
    $('.dropdown-menu').click(function (event) {
        event.stopPropagation();
    });
});

function ReleaseVM(group, instance_id, location) {
    //debugger;
    var self = this;
    if (typeof instance_id == 'undefined') {
        self.instances = ko.observableArray(group.instances.splice(0, group.quantity()));
        self.location_id = group.location_id();
    }
    else {
        self.instances = ko.observableArray();
        self.instances.push(instance_id);
        self.location_id = location;
    }
    self.id = group.id;
    self.property = group.property;
    self.property_str = group.property_str;
    self.rate = group.rate;
    self.location = ko.observable(location);

    self.count = function () {
        return self.instances().length;
    }
    self.get_location_name = function (locations) {
        var location = get_by_id(locations, self.location_id);
        if (location) {
            return location.name;
        } else {
            return '-';
        }
    }

}

function GroupVM(group) {
    var self = this;
    self.instances = ko.observableArray(group.instances);

    var property = {};
    if (typeof(group.property) != 'undefined') {
        property = JSON.parse(group.property);
    }
    self.rate = property.rate;
    delete property.rate;
    self.property = property;
    var json_str = JSON.stringify(property);
    self.property_str = json_str.substring(1, json_str.length - 1).replace(/"/g, '').replace(/,/g, ', ');
    self.count = function () {
        return self.instances().length;
    }
    self.quantity = ko.observable();
    self.location_id = ko.observable();
    self.id = group.property;

    self.valid = ko.computed(function () {
        if (isAN(self.quantity()) && self.quantity() > 0) {
            return true;
        }
        return false;
    });

}

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
            self.item_locations = ko.observableArray(data);
        }
    });

    self.item_locations_sans_store = ko.observableArray(self.item_locations().slice(0));
    self.item_locations_sans_store.remove(get_by_name(self.item_locations_sans_store(), 'Store'));

    self.all_item_instances = ko.observable({});

    $.ajax({
        url: '/inventory/item_instances.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.item_instances = ko.observableArray(data);
            for (var k in data) {
                var obj = data[k];
                var groups = [];
                for (var l in obj.groups) {
                    var group = obj.groups[l];
                    groups.push(new GroupVM(group));
                }
                self.all_item_instances()[obj.id] = ko.observableArray(groups);
                //debugger;
            }
        }
    });

    self.msg = ko.observable('');
    self.status = ko.observable('standby');

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.table_view = new TableViewModel({rows: data.rows, argument: self}, DemandRow);

    self.id.subscribe(function (id) {
        history.pushState(id, id, window.location.href + id + '/');
    });

    self.save = function (item, event) {
        if (!self.release_no()) {
            alert.error('Release No. is required!');
            return false;
        }
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
                    self.table_view.deleted_rows([]);
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
    self.groups = ko.observableArray();
    self.release_vms = ko.observableArray();
    self.demand_id = demand_vm.id();


    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

    self.ind = function () {
        if (demand_vm.table_view) {
            return demand_vm.table_view.rows().indexOf(self);
        }
    };

    self.item.subscribe(function (item) {
        if (!item) return;
        if (!self.specification())
            self.specification(item.description);
        if (!self.unit())
            self.unit(item.unit);
        self.inventory_account_id(item.account_no);
    });

    self.load_groups = function (val) {
        if (val) {
            if (typeof demand_vm.all_item_instances()[val] == 'undefined') {
                self.groups(null);
            } else {
                self.groups(demand_vm.all_item_instances()[val]());
            }
        }
    }


    self.load_groups(self.item_id());

    if (row) {
        //var vms = [];
        if (row.releases.length > 0) {
            for (var k in row.releases) {
                var release = row.releases[k];
                release.item_instance.properties['rate'] = release.item_instance.item_rate + '';
                var id = JSON.stringify(release.item_instance.properties);
                var group = get_by_id(self.groups(), id);
                if (typeof group == 'undefined') {
                    var group_data = {'instances': [], property: id};
                    var group = new GroupVM(group_data);
                    self.groups.push(group);
                }
                var match = null;
                var release_vm;
                for (var k in self.release_vms()) {
                    release_vm = self.release_vms()[k];
                    if (release_vm.id == id && release_vm.location_id == release.location) {
                        match = release_vm;
                        break;
                    }
                }

                if (match) {
                    release_vm.instances.push(release.item_instance.id);
                }
                else if (group) {
                    release_vm = new ReleaseVM(group, release.item_instance.id, release.location);
                    self.release_vms.push(release_vm);
                }
                if (release_vm) {
                    get_by_id(self.groups(), release_vm.id).instances.remove(release.item_instance.id);
                }
            }
        }
    }

    self.to_json = function () {
        self.index = self.ind();
        return ko.toJSON(self);
    }

    self.approve = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/approve/demand_form/',
            data: self.to_json(),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                    $($("#tbody > tr")[self.ind()]).addClass('invalid-row');
                }
                else {
                    alert.success('Approved!')
                    self.status('Approved');
                    $($("#tbody > tr")[self.ind()]).removeClass('invalid-row');
                    $(document).trigger('reload-selectize');
                }
            }
        });
    };

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
                    $(document).trigger('reload-selectize');
                }
            }
        });
    };

    self.fulfill = function (item, event) {
        //self.fulfill = function (root, item, event) {
        //if (root.release_no() == '' || !root.release_no()) {
        //    alert.error('Release No. is required!');
        //    return false;
        //}
        //root.save();
        $.ajax({
            type: "POST",
            url: '/inventory/fulfill/demand_form/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Set as Fulfilled!');
                    self.status('Fulfilled');
                }
            }
        });
    };

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
    };

    self.release_focused = function (row, e) {
        var target = $(e.currentTarget);
        //if (!e.isTrigger) {
        if (!target.parent().hasClass('open') && !target.is(":hover")) {
            target.parent().addClass('open');
        }
        //}
    };

    self.add = function (group) {

        var match = null;
        var release_vm;
        for (var k in self.release_vms()) {
            release_vm = self.release_vms()[k];
            if (release_vm.id == group.id && release_vm.location_id == group.location_id()) {
                match = release_vm;
                break;
            }
        }
        if (match) {
            release_vm.instances.push(group.instances.splice(0, group.quantity()));
        }
        else {
            var release = new ReleaseVM(group);
            self.release_vms.push(release);
        }
        group.quantity(null);
    }

    self.remove = function (release) {
        var group = get_by_id(self.groups(), release.id);
        ko.utils.arrayPushAll(group.instances, release.instances())
        self.release_vms.remove(release);
    }

    self.total_quantity = ko.computed(function () {
        var total = 0;
        if (self.groups().length) {
            for (var k in self.groups()) {
                var group = self.groups()[k];
                if (group.count) {
                    total += group.count();
                }
            }
        }
        return total;
    });

    self.total_release = ko.computed(function () {
        var total = 0;
        if (self.release_vms().length) {
            for (var k in self.release_vms()) {
                var release = self.release_vms()[k];
                total += release.count();
            }
        }
        return total;
    });

    self.item_id.subscribe(self.load_groups);

}

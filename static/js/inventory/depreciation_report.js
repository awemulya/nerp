$(document).ready(function () {
    vm = new DepreciationVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function DepreciationVM(data) {
    var self = this;
    self.table_view = new TableViewModel({rows: data}, DepreciationRow);


    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/inspection/',
            data: ko.toJSON(self),
            success: function (msg) {
                alert(msg)
                if (typeof (msg.error_message) != 'undefined') {
//                    $('#message').html(msg.error_message);
//                    self.msg();
                    alert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    alert.success('Saved!');
                    self.table_view.deleted_rows([]);
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

function DepreciationRow(row) {
    var self = this;
    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
    self.price = ko.computed(function () {
        return self.total_dr_amount() * self.rate()
    });
    self.depreciate = ko.toJS(self.depreciation())

    self.decay_duration = ko.computed(function () {
        var date1 = new Date(self.entry_date());
        var today = new Date();
        var timeDiff = Math.abs(today.getTime() - date1.getTime());
        var diff = Math.ceil(timeDiff / (1000 * 3600 * 24));
        return diff;
    });

    self.time = ko.computed(function () {
        if (self.depreciate.time_type == 'years') {
            return self.decay_duration() / 365;
        } else if (self.depreciate.time_type == 'months') {
            return self.decay_duration() / 30;
        } else {
            return self.decay_duration();
        }
    });

    self.decay_value = ko.computed(function () {
        if (self.depreciate.depreciate_type == 'Fixed percentage') {
            return (self.price() * self.time() * self.depreciate.depreciate_value) / (100 * self.depreciate.time);
        } else if (self.depreciate.depreciate_type == 'Compound percentage') {

        } else {
            return (self.time() * self.depreciate.depreciate_value / self.depreciate.time);
        }
    });

    self.current_value = ko.computed(function () {
        return self.price() - self.decay_value();
    });
}
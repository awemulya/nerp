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
    self.price = ko.computed(function() {
        return self.total_dr_amount() * self.rate()
    });
    self.depreciate = ko.toJS(self.depreciation())
    debugger;
}
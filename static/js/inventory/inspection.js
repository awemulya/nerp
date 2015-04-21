$(document).ready(function () {
    vm = new InspectionVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function InspectionVM(data) {

    var self = this;
	self.table_view = new TableViewModel({rows: data}, InspectionRow);


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

function InspectionRow(row) {

    var self = this;
    // self.sn = ko.observable();
    self.match_number = ko.observable();
    self.unmatch_number = ko.observable();
    self.decrement = ko.observable();
    self.increment = ko.observable();
    self.decrement_increment_price = ko.observable();
    self.good = ko.observable();
    self.bad = ko.observable();
    self.remarks = ko.observable();

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
    self.price = ko.computed(function() {
        return self.total_dr_amount() * self.rate()
    });
}
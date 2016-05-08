$(document).ready(function () {
    vm = new YearlyReportVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function YearlyReportVM(data) {

    var self = this;
    self.id = ko.observable(data.id);
    self.fiscal_year_id = ko.observable(data.fiscal_year);
    self.table_view = new TableViewModel({rows: data.rows}, YearlyReportRow);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/yearly_report_detail/',
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
            },
           // error: function(XMLHttpRequest, textStatus, errorThrown) {
           //     $('#message').html(XMLHttpRequest.responseText.message);
           // }
        });
    }
}

function YearlyReportRow(row) {

    var self = this;
    self.id = ko.observable()
    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
    // self.expense = ko.computed(function() {
    //     return localize(self.income() - self.remaining());
    // });

    self.remarks = ko.observable()
}
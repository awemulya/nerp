/**
 * Created by xtranophilist on 3/29/14.
 */

$(document).ready(function () {

    vm = new IncomingVM(ko_data);
    ko.applyBindings(vm);

    $('#id_record').selectize();

    $('#id_user').selectize();

});

function IncomingVM(data) {

    var self = this;
    self.user = ko.observable();
    self.record = ko.observable();
    self.borrow_date = ko.observable();
    self.due_date = ko.observable();
    self.return_date = ko.observable();
    self.fine_per_day = ko.observable();
    self.fine_paid = ko.observable();

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

    self.total_fine = function () {
        var one_day = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds

        if (self.return_date()) {
            var return_date = new Date(self.return_date().replace(/\b(\d{1})\b/g, '0$1'));
        }
        else {
            //if today is earlier than due date
            if (new Date().getTime() < new Date(self.due_date().replace(/\b(\d{1})\b/g, '0$1')).getTime())
                return 0;
            var return_date = new Date();
        }

        var days = Math.floor(
            (return_date.getTime() - new Date(self.due_date().replace(/\b(\d{1})\b/g, '0$1')).getTime()) / one_day
        );

        if (days < 0)
            days = 0;

        return days * self.fine_per_day();

    }

}



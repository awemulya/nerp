$(document).ready(function () {
    vm = new DisbursementVM(ko_data);
    ko.applyBindings(vm);
});


function DisbursementVM(data) {
    var self = this;
    self.data = data;
}
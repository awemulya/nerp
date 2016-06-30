$(document).ready(function () {
    vm = new DisbursementVM(ko_data);
    ko.applyBindings(vm);
});

function ModeVM(data) {
    var self = this;
    self.key = data.key;
    self.name = data.value.name;
    self.disbursements = data.value.disbursements;
    self.nrs_subtotal = 0;
    self.usd_subtotal = 0;
    self.sdr_subtotal = 0;
    ko.utils.arrayForEach(self.disbursements, function (disbursement) {
        self.nrs_subtotal += parseFloat(disbursement.nrs);
        self.usd_subtotal += parseFloat(disbursement.usd);
        self.sdr_subtotal += parseFloat(disbursement.sdr);
    });
    return self;
}

function DisbursementVM(data) {
    var self = this;
    self.data = data;

    self.initial_deposit = data.initial_deposit;

    self.modes = ko.observableArray([]);

    self.nrs_total = 0;
    self.usd_total = 0;
    self.sdr_total = 0;

    ko.utils.arrayForEach(dict_to_arr(data.modes), function (mode) {
        var mode_vm = new ModeVM(mode);
        self.modes.push(mode_vm);
        self.nrs_total += parseFloat(mode_vm.nrs_subtotal);
        self.usd_total += parseFloat(mode_vm.usd_subtotal);
        self.sdr_total += parseFloat(mode_vm.sdr_subtotal);
    });


}
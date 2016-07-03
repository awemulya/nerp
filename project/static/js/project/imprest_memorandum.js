$(document).ready(function () {
    vm = new ImprestMemo(ko_data);
    ko.applyBindings(vm);
});

function ImprestMemo(data) {
    var self = this;
    self.data = data;

    self.fy_end_nrs = parseFloat(data.fy_end_balance[0]);
    self.fy_end_exchange_rate = parseFloat(data.fy_end_exchange_data.rate);
    self.fy_end_usd = round2(self.fy_end_nrs * self.fy_end_exchange_rate);

    self.disbursement_party_nrs = parseFloat(data.disbursements[0][0]);
    self.disbursement_party_usd = parseFloat(data.disbursements[0][1]);
    self.disbursement_gon_nrs = parseFloat(data.disbursements[1][0]);
    self.disbursement_gon_usd = parseFloat(data.disbursements[1][1]);


}
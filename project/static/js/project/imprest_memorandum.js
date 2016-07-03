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
    self.disbursement_total_nrs = round2(self.disbursement_gon_nrs + self.disbursement_party_nrs);
    self.disbursement_total_usd = round2(self.disbursement_gon_usd + self.disbursement_party_usd);
    
    self.replenishment_party_nrs = parseFloat(data.replenishments[0][0]);
    self.replenishment_party_usd = parseFloat(data.replenishments[0][1]);
    self.replenishment_gon_nrs = parseFloat(data.replenishments[1][0]);
    self.replenishment_gon_usd = parseFloat(data.replenishments[1][1]);
    self.replenishment_total_nrs = round2(self.replenishment_gon_nrs + self.replenishment_party_nrs);
    self.replenishment_total_usd = round2(self.replenishment_gon_usd + self.replenishment_party_usd);
    
    self.liquidation_party_nrs = parseFloat(data.liquidations[0][0]);
    self.liquidation_party_usd = parseFloat(data.liquidations[0][1]);
    self.liquidation_gon_nrs = parseFloat(data.liquidations[1][0]);
    self.liquidation_gon_usd = parseFloat(data.liquidations[1][1]);
    self.liquidation_total_nrs = round2(self.liquidation_gon_nrs + self.liquidation_party_nrs);
    self.liquidation_total_usd = round2(self.liquidation_gon_usd + self.liquidation_party_usd);
}
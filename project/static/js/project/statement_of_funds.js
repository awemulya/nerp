$(document).ready(function () {
    vm = new FundVM(ko_data);
    ko.applyBindings(vm);
});

function BudgetUsage(usages) {
    var self = this;
    self.usages = usages;
    self.release_total = 0;
    self.unspent_total = 0;

    ko.utils.arrayForEach(usages, function (usage) {
        self.release_total += parseFloat(usage.release);
        self.unspent_total += parseFloat(usage.release) - parseFloat(usage.spent);
    });
}

function FundVM(data) {
    var self = this;
    self.data = data;
    self.budget_usage = new BudgetUsage(data.budget_usage);
}
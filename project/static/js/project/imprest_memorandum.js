$(document).ready(function () {
    vm = new ImprestMemo(ko_data);
    ko.applyBindings(vm);
});

function ImprestMemo(data) {
    var self = this;
    self.data = data;

    


}
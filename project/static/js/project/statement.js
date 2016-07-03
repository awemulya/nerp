$(document).ready(function () {
    vm = new Statement(categories);
    ko.applyBindings(vm);
});

function Statement(categories) {
    var self = this;
    self.categories = categories;
    console.log(self.categories)

    


}
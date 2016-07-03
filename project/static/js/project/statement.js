$(document).ready(function () {
    vm = new Statement(categories);
    ko.applyBindings(vm);
});

function Statement(categories) {
    var self = this;
    self.categories = categories;
    self.categories_sub_total = function() {
        var sum = 0;
        for (var index=0; index < categories.length; index++) 
            sum += categories[index].subtotal;
        return sum
    };

}
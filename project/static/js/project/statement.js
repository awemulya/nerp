$(document).ready(function () {
    vm = new Statement(ko_data);
    ko.applyBindings(vm);
});

function Statement(data) {
    var self = this;
    self.categories = data.categories;
    self.categories_sub_total = function() {
        var sum = 0;
        for (var index=0; index < categories.length; index++)
            sum += categories[index].subtotal;
        return sum
    };

}
$(document).ready(function () {
    vm = new InlineForm();
    ko.applyBindings(vm);
});

function InlineForm() {
    //debugger;
    var self = this;

    
    self.added_rows = ko.observableArray([]);
    self.add_row = function(){
        self.added_rows.push(self.added_rows().length)
    };
    self.remove_row = function(row){
        self.added_rows.remove(row);
    };

    
};

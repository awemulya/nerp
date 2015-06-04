$(document).ready(function () {
    item = new ItemVM(item_data);
    // ko.applyBindings(item);
    var item_form = document.getElementById("item_form");
    debugger;
    // ko.cleanNode(item_form);
    ko.applyBindings(item, item_form);
    $('.change-on-ready').trigger('change');
});

function ItemVM(data) {
    var self = this;
    for (var k in data)
        self[k] = ko.observable(data[k]);
    self.opening_balance = ko.observable();

	self.other_properties = ko.observableArray([new OtherPropertiesVM()]);
	
	self.addOtherProperty = function () {
			self.other_properties.push(new OtherPropertiesVM());
	    };

	self.removeOtherProperty = function(property){
		self.other_properties.remove(property);
	};

}

function OtherPropertiesVM() {
	// debugger;

    var self = this;
    self.property_name = ko.observable();
    self.property = ko.observable();
}    	
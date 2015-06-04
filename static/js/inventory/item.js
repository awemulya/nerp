$(document).ready(function () {
    item = new ItemVM(item_data);
    // ko.applyBindings(item);
    var item_form = document.getElementById("other-properties");
    // ko.cleanNode(item_form);
    ko.applyBindings(item, item_form);
    $('.change-on-ready').trigger('change');
});

function ItemVM(data) {
    var self = this;
    self.opening_balance = ko.observable();
	self.other_properties = ko.observableArray([]);
    
    if (data != null) {
    	// var test = JSON.parse(data);
    	for (item_property in data) {
    		var property_name = item_property
    		var property = data[item_property]
    		self.other_properties.push(new OtherPropertiesVM().property_name(property_name).property(property))
    	}
    	// debugger;
    } else {
    	self.other_properties.push(new OtherPropertiesVM())
    }
	
	self.addOtherProperty = function () {
			self.other_properties.push(new OtherPropertiesVM());
	    };

	self.removeOtherProperty = function(property){
		self.other_properties.remove(property);
	};

}

function OtherPropertiesVM() {
    var self = this;
    self.property_name = ko.observable();
    self.property = ko.observable();
}    	
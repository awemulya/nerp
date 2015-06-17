$(document).ready(function () {
    if (typeof(item_data) == "undefined") {
    	item = new ItemVM();
    } else {
    	item = new ItemVM(item_data);
    }
    if (typeof(depreciation_data) == "undefined") {
        depreciate = new ItemVM();
    } else {
        depreciate = new DepreciationVM(depreciation_data);
    }

    // ko.applyBindings(item);
    var item_form = document.getElementById("other-properties");
    var depreciation_form = document.getElementById("depreciation")
    // ko.cleanNode(item_form);
    ko.applyBindings(item, item_form);
    ko.applyBindings(depreciate, depreciation_form)
    $('.change-on-ready').trigger('change');
});

function DepreciationVM(data) {
    for (var k in data) {
        if (data[k] != null)
            self[k] = ko.observable(data[k]);
    }
}

function ItemVM(data) {
    var self = this;
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
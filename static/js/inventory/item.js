$(document).ready(function () {
    if (typeof(item_data) == "undefined") {
        item = new ItemVM();
    } else {
        item = new ItemVM(item_data);
    }
    // if (typeof(depreciation_data) == "undefined") {
    //     depreciate = new ItemVM();
    // } else {
    //     depreciate = new DepreciationVM(depreciation_data);
    // }
    
    depreciate = new DepreciationVM(depreciation_data);
    var item_form = document.getElementById("other-properties");
    var depreciation_form = document.getElementById("depreciation")
    ko.applyBindings(item, item_form);
    ko.applyBindings(depreciate, depreciation_form)
    $('.change-on-ready').trigger('change');
});

function DepreciationVM(data) {
    self = this;
    for (var k in data) {
        if (data[k] != null)
            self[k] = ko.observable(data[k]);
    }
    self.postfix = ko.computed( function () {
            if (self.depreciate_type() == 'Fixed percentage' || self.depreciate_type() == 'Compounded percentage'){
                return '%'
            } else {
                return '/-'
            }
        });
}

function ItemVM(data) {
    var self = this;
	self.other_properties = ko.observableArray([]);
    
    if (data != null) {
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
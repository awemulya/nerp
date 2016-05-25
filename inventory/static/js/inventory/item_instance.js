$(document).ready(function () {
    if (typeof(item_data) == "undefined") {
        item = new ItemInstanceVM();
    } else {
        item = new ItemInstanceVM(item_data);
    }
    var item_form = document.getElementById("other-properties");
    ko.applyBindings(item, item_form);
    $('.change-on-ready').trigger('change');
});

function ItemInstanceVM(data) {
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
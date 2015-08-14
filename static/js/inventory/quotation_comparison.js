$(document).ready(function () {
    vm = new QuotationComparisonVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function QuotationComparisonVM(data){
	var self = this;

	$.ajax({
		url: '/inventory/items.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			self.items = ko.observableArray(data);
		}
	});

	$.ajax({
		url: '/parties.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			self.parties = ko.observableArray(data);
		}
	});
	
	self.selected_party = ko.observable()
	self.party_display = ko.observableArray([])

	self.add_party = function () {
		for (o in self.parties() ){
			if (self.parties()[o].id == self.selected_party()) {
				self.party_display.push(self.parties()[o]);
			}
		}
	}

    for (i in data.rows) {
    	self.party_display.push(data.rows[i].party.party)
    }

    self.table_view = new TableViewModel({rows: data.rows}, QuotationRow);

	self.item_changed = function (row) {
		var selected_item = $.grep(self.items(), function (i) {
			return i.id == row.item_id();
		})[0];
		if (!selected_item) return;
		if (!row.specification())
			row.specification(selected_item.description);
		if (!row.unit())
			row.unit(selected_item.unit);
		row.inventory_classification_reference_no(selected_item.property_classification_reference_number);
		row.account_no(selected_item.account_no);
	}

    for (var k in data)
        self[k] = ko.observable(data[k]);


}

function PartyQuotationVM(party) {
	var self = this;
	self.per_unit_price = ko.observable();

}

function QuotationRow(row) {
	var self = this;
	self.item_id = ko.observable()
	self.specification = ko.observable()
	self.remarks = ko.observable()
	self.quantity = ko.observable()
	self.estimated_cost = ko.observable()
    // debugger;
    self.unit = ko.observable()
    self.inventory_classification_reference_no = ko.observable()
    self.account_no = ko.observable()

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

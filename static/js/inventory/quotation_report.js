$(document).ready(function () {
    vm = new QuotationReportVM();
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function QuotationReportVM(data){
	var self = this;

	$.ajax({
		url: '/inventory/items.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			self.items = ko.observableArray(data);
		}
	});
    
    self.table_view = new TableViewModel({}, QuotationRow);

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


}

function QuotationRow(row) {
	var self = this
}
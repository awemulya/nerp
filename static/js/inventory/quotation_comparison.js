$(document).ready(function () {
    vm = new QuotationComparisonVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function QuotationComparisonVM(data){
	var self = this;
    // debugger;

	// $.ajax({
	// 	url: '/inventory/items.json',
	// 	dataType: 'json',
	// 	async: false,
	// 	success: function (data) {
	// 		self.items = ko.observableArray(data);
	// 	}
	// });
    
    self.table_view = new TableViewModel({rows: data.rows}, QuotationRow);

	// self.item_changed = function (row) {
	// 	var selected_item = $.grep(self.items(), function (i) {
	// 		return i.id == row.item_id();
	// 	})[0];
	// 	if (!selected_item) return;
	// 	if (!row.specification())
	// 		row.specification(selected_item.description);
	// 	if (!row.unit())
	// 		row.unit(selected_item.unit);
	// 	row.inventory_classification_reference_no(selected_item.property_classification_reference_number);
	// 	row.account_no(selected_item.account_no);
	// }


}

function QuotationRow(row) {
	var self = this;

    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
    // debugger;
}
$(document).ready(function () {
    vm = new QuotationComparisonVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function QuotationComparisonVM(data){
	var self = this;
    // debugger;

	$.ajax({
		url: '/inventory/items.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			self.items = ko.observableArray(data);
		}
	});

	$.ajax({
		url: '/inventory/party.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			debugger
			self.parties = ko.observableArray(data);
		}
	});
    
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


}

function QuotationRow(row) {
	var self = this;
	self.item_id = ko.observable()
	self.specification = ko.observable()
	self.quantity = ko.observable()
	self.estimated_cost = ko.observable()
	
    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
    debugger;
}
// <table class="table table-bordered table-striped">
	// <thead>
	// 	<tr>
	// 		<th rowspan='3'>{% trans 'SN' %}</th>
	// 		<th rowspan='3'>{% trans 'Item Name' %}</th>
	// 		<th rowspan='3'>{% trans 'Specification' %}</th>
	// 		<th rowspan='3'>{% trans 'Item Quantity' %}</th>
	// 		<th rowspan='3'>{% trans 'Estimated Cost' %}</th>
	// 		<th colspan='6'>{% trans "Bidder's Quoted Price" %}</th>
	// 		<th rowspan='3'>{% trans "Remarks" %}</th>
	// 	</tr>
	// 	<tr>
	// 		<th colspan='2'>{% trans "Gauri Shanar" %}</th>
	// 		<th colspan='2'>{% trans "Gauri Shanar" %}</th>
	// 		<th colspan='2'>{% trans "Gauri Shanar" %}</th>
	// 	</tr>
	// 	<tr>
	// 		<th>{% trans "Per Unit Price" %}</th>
	// 		<th>{% trans "Total Price" %}</th>
	// 		<th>{% trans "Per Unit Price" %}</th>
	// 		<th>{% trans "Total Price" %}</th>
	// 		<th>{% trans "Per Unit Price" %}</th>
	// 		<th>{% trans "Total Price" %}</th>

	// 	</tr>

	// </thead>
	// <tbody>
 //                <!-- ko foreach: rows -->

	// 	<tr>
	// 		<td>
	//             <span class="wid-pad pull-left" data-bind="text:  $index()+1, localize: true"> </span>
	// 		</td>
 			// <td>
    //             <select data-bind="selectize: $root.items, value: item_id, object: item, event: {change: $root.item_changed}"
    //                             data-url="{% url 'create_inventory_item' %}"
    //                             data-script="/static/js/inventory/item.js"></select>
    //                     {#                                                <select class="span12 item-selector"#}
    //                     {#                                                        data-bind="options: $root.items, optionsText: 'name', optionsValue: 'id', value: item_id, optionsCaption: ' ', event: {change: $root.item_changed}"></select>#}
    //                     {#                        <input type="hidden" data-url="{% url 'create_inventory_item' %}" class="change-on-ready"#}
    //                     {#                               data-bind="value: item_id, select2: $root.items, event: {change: $root.item_changed}, readOnly: status() != 'Requested'">#}
    //         </td>

	// 	</tr>
 //               <!-- /ko -->

	// </tbody>
// </table>
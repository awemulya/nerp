$(document).ready(function () {
    vm = new QuotationComparisonVM(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function QuotationComparisonVM(data){
	var self = this;

    self.release_no = ko.observable();
    self.id = ko.observable()

	$.ajax({
		url: '/inventory/items.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			self.items = ko.observableArray(data);
		}
	});


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

	$.ajax({
		url: '/parties.json',
		dataType: 'json',
		async: false,
		success: function (data) {
			self.parties = ko.observableArray(data);
		}
	});

	self.selected_party = ko.observable()

	self.parties_to_display = ko.observableArray([])

	self.add_party = function (row) {
		for (o in self.parties()){
			if (self.parties()[o].id == self.selected_party()) {
				self.parties_to_display.push(self.parties()[o]);
				for ( qr in row.rows()){
					row.rows()[qr].bidder_quote.push(new PartyQuotationVM().bidder_name(self.parties()[o].name))
				}
			}
		}
		self.parties.remove( function(item) {return item.id == self.selected_party() })
	}

	self.removeParty = function(party) {
		self.parties_to_display.remove(party)
		self.parties.push(party)
		for ( o in self.table_view.rows()){
			self.table_view.rows()[o].bidder_quote.remove( function(item) {
				return item.bidder_name() === party.name
			});
		}
	}
    self.table_view = new TableViewModel({rows: data.rows, argument: self.parties_to_display() }, QuotationRow);

    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/quotation-comparison/',
            data: ko.toJSON(self),
            success: function (msg) {
                alert(msg)
                if (typeof (msg.error_message) != 'undefined') {
//                    $('#message').html(msg.error_message);
//                    self.msg();
                    alert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    alert.success('Saved!');
                    if (msg.id)
                        self.id(msg.id);
                    $("#tbody > tr").each(function (i) {
                        $($("#tbody > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        for (var j in self.table_view.rows()[i].bidder_quote()){
                        	self.table_view.rows()[i].bidder_quote()[j].id = msg.party[j]
                        }
                        $($("#tbody > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
//            error: function(XMLHttpRequest, textStatus, errorThrown) {
//                $('#message').html(XMLHttpRequest.responseText.message);
//            }
        });
    }
    for (var k in data) {
    if (data[k] != null)
        self[k] = ko.observable(data[k]);
	}

	if ( data.rows != '' ){
	    for (var j in data.rows[0].bidder_quote) {
	    	// debugger;
	    	self.parties_to_display.push(data.rows[0].bidder_quote[j].party)
			// self.bidder_quote.push(new PartyQuotationVM().bidder_name(data.rows[i].party.party.name))
	    }
    }
}

function PartyQuotationVM() {
	var self = this;
	self.id = ko.observable()
	self.bidder_name = ko.observable();
	self.per_unit_price = ko.observable();
}



function QuotationRow(row, argument) {
	var self = this;

	self.item_id = ko.observable()
	self.specification = ko.observable()
	self.estimated_cost = ko.observable()
	self.quantity = ko.observable()
    self.unit = ko.observable()
    self.inventory_classification_reference_no = ko.observable()
    self.account_no = ko.observable()
	self.remarks = ko.observable()

    self.bidder_quote = ko.observableArray()
    if ( argument ){
    	for (o in argument) {
    		self.bidder_quote.push(new PartyQuotationVM().bidder_name(argument[o].name))
    	}
    }

    // if( row.party ) {
    // 	self.bidder_quote.push(row.party)
    // }
	
    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }

}

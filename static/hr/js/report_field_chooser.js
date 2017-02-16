// Dependencies
// App.js and its dependencies and knockout js
// App.js
// End Dependencies


var optionVM = function (options, selected, main_vm) {
    var self = this;
    self.options = ko.observableArray(options);
    self.selected = ko.observable(selected);
    
    self.selected.subscribe(function () {
        console.log(self.selected());
        main_vm.compute_query()
        
    })
};


var mainVM = function (params) {
    var self = this;
    // if params.query populate optionvm
    self.option_vms = ko.observableArray();
    self.query = params.value_obs;

    self.get_child_options = function () {
        var url = '/payroll/get-report-field/';
        App.showProcessing();

        App.remotePost(url, {'query': self.query()}, function (response) {
            App.hideProcessing();
            self.option_vms.push(new optionVM(response.options, null, self));
            console.log('success');
        }, function () {
            App.hideProcessing();
            console.log(errorThrown);
        });
    };
    self.compute_query = function(){
        var total_qry = '';
        ko.utils.arrayForEach(self.option_vms(), function (option_vm) {
            total_qry += option_vm.selected();
        });
        self.query(total_qry);
    };

    if (!self.query()){
        self.get_child_options();
    }

    self.query.subscribe(function () {
        // debugger;
        if (self.query().slice(-3) == '___' || self.query().slice(-2) == '__') {
            self.get_child_options()

        }
    });
};

ko.components.register('report-field-chooser', {
    viewModel: mainVM,
    template: '<div class="row">'

    + '<!-- ko foreach: option_vms -->'
    + '<select data-bind="options: options, optionsText: function(item){return item[1];}, optionsValue: function(item){ return item[0];},  value: selected">'
    + '<select>'
    + '<!-- /ko -->'
    + '</div>'
});


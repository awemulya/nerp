// Dependencies
// App.js and its dependencies and knockout js
// Requires modal custom binding
// End Dependencies


var optionVM = function(){
    var self = this;
    self.options = ko.observableArray();
    self.selected = ko.observable();
    self.order = ko.observable();
};


var mainVM = function (params) {
    var self = this;
    self.modal_name = ko.observable(params.modal_name);
    self.show_modal = ko.observable(false);
    self.closeRecordModal = function () {
        self.show_modal(false);
    };
    self.select_list = params.select_list_obs;
    self.selected_item = params.selected_item_obs;
    self.optionsCaption = params.optionsCaption;
    self.optionsText = params.optionsText;
    // self.optionsValue = params.optionsValue;
    self.form_observables = params.form_observables;
    var api_url = params.api_url;

    self.form_vm = ko.observable(new modalFormVm(self.form_observables, self.select_list, self.show_modal, api_url));

    self._add = function () {
        self.show_modal(true);
        self.form_vm(new modalFormVm(self.form_observables, self.select_list, self.show_modal, api_url, null, self.selected_item));

    };
    self._update = function () {
        self.form_vm(self.selected_item());
        self.show_modal(true);
    };


    self.computed_modal_name = ko.computed(function () {
        if (self.form_vm().id()) {
            self.modal_name('Edit ' + params.modal_name);
        } else {
            self.modal_name('Add New ' + params.modal_name);
        }
    });

    // Load grade scale
    loadList(api_url, function (res) {
        var items = ko.utils.arrayMap(res, function (item) {
            return new modalFormVm(self.form_observables, self.select_list, self.show_modal, api_url, item);
        });
        self.select_list([]);
        self.select_list(items);
        App.hideProcessing();
    });
    // End Load grade scale
};

ko.components.register('report-field-chooser', {
    viewModel: mainVM,
    template: '<div class="input-group">'
    + '<select class="form-control" aria-describedby="basic-addon2" data-bind="options : select_list, value: selected_item, optionsCaption: optionsCaption, optionsText: optionsText"> </select>'
    + '<span class="input-group-btn">'
    + '<button type="button" data-bind="click: _add" class="btn btn-raised btn-primary"aria-label="Add Validity">'
    + '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>'
    + '</button>'
    + '<!-- ko if: selected_item() -->'
    + '<button type="button" data-bind="click: _update" class="btn btn-raised btn-primary"'
    + 'aria-label="Update Validity">'
    + '<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>'
    + '</button>'
    + '<!-- /ko -->'
    + '</span>'
    + '</div>'
    + '<div class="modal fade" data-bind="modal: show_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">'
    + '<div class="modal-dialog">'
    + '<div class="modal-content">'
    + '<div class="modal-header">'
    + '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
    + '<h4 class="modal-title to_uppercase">'
    + '<span data-bind="text: modal_name"></span>'
    + '</h4>'
    + '</div>'

    + '<div class="modal-body">'
    + '<!-- ko template: { nodes: $componentTemplateNodes, data: form_vm() } --><!-- /ko -->'

    + '<!-- ko if: typeof(form_vm().id()) == "undefined" -->'
    + '<br>'
    + '<input type="button" class="btn btn-raised btn-primary" value="Save" data-bind="click: form_vm().save">'
    + '<!-- /ko -->'
    + '<!-- ko if: typeof(form_vm().id()) != "undefined" -->'
    + '<input type="button" class="btn btn-raised btn-primary" value="Update" data-bind="click: form_vm().update">'
    + '<input type="button" class="btn btn-raised btn-danger" value="Delete" data-bind="click: form_vm()._delete">'
    + '<!-- /ko -->'

    + '</div>'
    + '<div class="modal-footer">'

    + '</div>'
    + '</div>'
    + '</div>'
    + '</div>'
});


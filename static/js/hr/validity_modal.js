var validityModalVM  = function(params) {
    var self = this;
    self.modal_name = ko.observable(params.modal_name);
    self.show_modal = params.show_modal;
    self.closeRecordModal = function() {
        self.show_modal(false);
    };
    self.form_vm = params.form_vm;
    self.computed_modal_name = ko.computed(function(){
        if(self.form_vm().id()){
            self.modal_name('Edit ' + params.modal_name);
        }else{
            self.modal_name('Add New ' + params.modal_name);
        }
    });
};


ko.components.register('validity-modal', {
    viewModel: validityModalVM,
    template:'<div class="modal fade" data-bind="modal: show_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">'
	    +'<div class="modal-dialog">'
	        +'<div class="modal-content">'
	            +'<div class="modal-header">'
	                +'<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>'
	                +'<h4 class="modal-title to_uppercase">'
	                	+'<span data-bind="text: modal_name"></span>'
	                +'</h4>'
	            +'</div>'

	            +'<div class="modal-body">'
                        + '<!-- ko template: { nodes: $componentTemplateNodes, data: form_vm } --><!-- /ko -->'
	            +'</div>'

	            +'<div class="modal-footer">'
            	+'</div>'
	        +'</div>'
	    +'</div>'
	+'</div>'
});


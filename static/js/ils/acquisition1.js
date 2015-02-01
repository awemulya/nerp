$(document).ready(function () {
    acq = new AcquisionVM();
	    ko.applyBindings(acq);
	    });
AcquisionVM = function(){
	self = this;
	self.books = ko.observableArray();
	self.subjects = ko.observableArray();
	self.authors = ko.observableArray();
	self.pub_places = ko.observableArray();
	self.publishers = ko.observableArray();
	self.languages = ko.observableArray();

	self.ajaxPost = function(url, optionField, oble, selectize_element, formElement){
			var x = $('input, select').serialize();
			$.post(url,x
				).success(function(data){
					console.log(data);
					createdObj = {
						text: data[optionField],
						value: data.id,
					};
					self[oble].push(createdObj);

					var $select = $(selectize_element).selectize({
					});
					var selectize = $select[0].selectize;
					selectize.addOption(createdObj);
					selectize.addItem(data.id);

					var hh = $(formElement).find('.close-reveal-modal');
					$(hh).trigger("click");

				}).done(function(){
					var errorHtml = '<div data-alert class="alert-box success"><label> Option successfully ADDED and SELECTED!</label> <a href="#" class="close">&times;</a></div>';
					$('#main-error-area').append(errorHtml).foundation();
					// $('#main-error-area').fadeOut(6000, "swing");
				}).error(function(data){
					var errorHtml = '<div data-alert class="alert-box round">'+ data.responseText +'<a href="#" class="close">&times;</a></div>';
					$(formElement).append(errorHtml);
				});
		};

};
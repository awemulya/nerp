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

};
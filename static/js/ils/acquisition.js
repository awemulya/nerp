/**
 * Created by xtranophilist on 3/29/14.
 */

$(document).ready(function () {
    vm = new AcquisitionVM(ko_data);
    ko.applyBindings(vm);

    var new_create = function (input) {
        return {
            value: input,
            text: input
        }
    }

    $('#authors').selectize({
            plugins: ['remove_button'],
            create: new_create
        }
    );

    $('#subjects').selectize({
            create: new_create,
            plugins: ['remove_button']
        }
    );

    $('#books').selectize({
            create: new_create
        }
    );

    $('#publisher').selectize({
            create: new_create
        }
    );

});

function AcquisitionVM(data) {

    var self = this;
    self.isbn13 = ko.observable();
    self.book = ko.observable({subjects: [], id: null, subtitle: ''});
    self.publisher_id = ko.observable();
    self.edition = ko.observable();
    self.pagination = ko.observable();
    self.price = ko.observable();
    self.quantity = ko.observable(1);
    self.excerpt = ko.observable();
    self.notes = ko.observable();
    self.lcc = ko.observable();
    self.ddc = ko.observable();
    self.format = ko.observable();
    self.authors = ko.observableArray([]);
    self.languages = ko.observableArray([]);
    self.get_by_isbn = function(formElement){
        console.log('this is isbn'+ self.isbn13());
        var url = 'https://www.googleapis.com/books/v1/volumes?q=search+isbn'+self.isbn13();
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data){
                console.log('this is result'+data);
            }, 
            error: function(data){
                console.log('this is error'+data);
            },
        });

    };

    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }

//    if (self.book)
//        self.book = self.book();

    self.year = ko.observable('');
    self.month = ko.observable('');
    self.day = ko.observable('');


    if (self.date_of_publication)
        self.year(new Date(self.date_of_publication()).getFullYear());

    if (self.publication_has_month && self.publication_has_month())
        self.month(new Date(self.date_of_publication()).getMonth() + 1);

    if (self.publication_has_month && self.publication_has_day())
        self.day(new Date(self.date_of_publication()).getDate());

    $.ajax({
        url: '/library/authors.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.all_authors = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/library/publishers.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.publishers = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/languages.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.all_languages = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/library/books.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.books = ko.observableArray(data);
        }
    });

    $.ajax({
        url: '/library/subjects.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.subjects = ko.observableArray(data);
        }
    });


}


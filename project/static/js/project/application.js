$(document).ready(function () {
    vm = new ApplicationVM(ko_data);
    ko.applyBindings(vm);
});

function RowVM(data, category_vm) {
    var self = this;

    self.category_id = data.category;
    self.id = ko.observable(data.id);
    self.amount = ko.observable(data.amount);
    self.expense_id = ko.observable(data.expense);
    self.expense = ko.observable();
    self.klass = ko.observable();

    self.get_code = function () {
        if (self.expense()) {
            return self.expense().code();
        }
    };

    self.render_item = function (obj) {
        var expense = category_vm.get_expense_by_id(obj.id);
        return '<div>' + expense.original_name + '</div>';
    };

    self.render_option = function (obj) {
        var expense = category_vm.get_expense_by_id(obj.id);
        return '<div>' + expense.code() + ' - ' + expense.name() + '</div>';
    };
}

function ExpenseVM(data) {
    var self = this;
    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }
    self.original_name = self.name() + '';

    self.name(self.code() + ' - ' + self.name());

}

function CategoryVM(category_instance, expenses) {
    var self = this;
    self.instance = category_instance;

    self.full_name = function () {
        var st = self.instance.name
        if (self.instance.code) {
            st += ' - ' + self.instance.code;
        }
        if (self.instance.gon_funded) {
            st += ' (100% GON)';
        }
        return st;

    }

    self.rows = ko.observableArray();

    self.add_row = function (data) {
        data.category = self.instance.id;
        self.rows.push(new RowVM(data, self));
    }

    self.expenses = ko.computed(function () {
        return ko.utils.arrayFilter(expenses, function (expense) {
            return expense.category().indexOf(self.instance.id) != -1;

        });
    });

    self.get_expense_by_id = function (id) {
        return ko.utils.arrayFirst(self.expenses(), function (obj) {
            return obj.id() == id;
        })
    };

    self.remove_row = function (row) {
        self.rows.remove(row);
    }
}

function ApplicationVM(data) {
    var self = this;

    self.status = ko.observable('Loading...');

    //self.table_view = new TableViewModel({rows: data.rows, argument: self, auto_add_first: false}, ExpenseRow);

    self.fy_id = ko.observable(data.fy_id);

    self.categories = ko.observableArray();

    self.expenses = ko.observableArray();

    ko.utils.arrayForEach(data.expenses, function (obj) {
        self.expenses.push(new ExpenseVM(obj));
    });

    ko.utils.arrayForEach(data.categories, function (category) {
        self.categories.push(new CategoryVM(category, self.expenses()));
    });


    self.get_category_by_id = function (id) {
        return ko.utils.arrayFirst(self.categories(), function (obj) {
            return obj.instance.id == id;
        })
    };

    ko.utils.arrayForEach(data.rows, function (row) {
        self.get_category_by_id(row.category).add_row(row);
    });


    self.sort = function () {
        // Sort ascending by date
        self.table_view.rows.sort(function (l, r) {
            var l_date = new Date(l.date());
            var r_date = new Date(r.date());
            return l_date.getTime() > r_date.getTime();
        });

        // Always keep initial_deposit on top
        self.table_view.rows.sort(function (l, r) {
            return r.type() == 'initial_deposit';
        });
    };

    //self.sort();

    self.status('Ready');

    self.save = function () {
        //self.sort();
        $.ajax({
            type: "POST",
            url: '/project/application/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');
                    self.status('Saved');
                    ko.utils.arrayForEach(self.categories(), function (category) {
                        ko.utils.arrayForEach(category.rows(), function (row) {
                            row.klass('invalid-row');
                        });
                    });
                    for (var i in msg.categories) {
                        //debugger;
                        for (var j in msg.categories[i].rows) {
                            self.categories()[i].rows()[j].id(msg.categories[i].rows[j]);
                            self.categories()[i].rows()[j].klass('');
                        }
                    }
                    //self.table_view.deleted_rows([]);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert.error(textStatus.toTitleCase() + ' - ' + errorThrown);
            }
        });
    }

}
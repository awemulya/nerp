$(document).ready(function () {

    var new_create = function (input) {
        return {
            value: input,
            text: input
        }
    }

    var $selectized = {}

    $selectized['categories'] = $('#id_categories').selectize({
            plugins: ['remove_button']
        }
    )[0].selectize;

    $selectized['target_groups'] = $('#id_target_groups').selectize({
            plugins: ['remove_button']
        }
    )[0].selectize;

    $selectized['resource_persons'] = $('#id_resource_persons').selectize({
            plugins: ['remove_button']
        }
    )[0].selectize;

    $('.selectize').each(function (index) {
        var $sel = $(this).selectize()[0].selectize;
        init_selectize($sel);
    });


    var override_form = function (e, $form, key) {
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),

            success: function (obj, status) {
                $selectized[key].addOption({
                    text: obj.name,
                    value: obj.id
                });
                $selectized[key].addItem(obj.id);
                $form.closest('.reveal-modal').foundation('reveal', 'close');
//                $categories.refreshItems();
            }
        });

        e.preventDefault();
    }


    $('#add-category form').submit(function (e) {
        override_form(e, $(this), 'categories');
    });

    $('#add-target-group form').submit(function (e) {
        override_form(e, $(this), 'target_groups');
    });

    $('#add-resource-person form').submit(function (e) {
        override_form(e, $(this), 'resource_persons');
    });

    var training_vm = new TrainingVM();
    ko.applyBindings(training_vm, $('#participants')[0]);
    training_vm.available = $('#available').selectize()[0].selectize;

    vm = new FilesVM(vm_files);
    ko.applyBindings(vm, $('#files')[0]);

    var date_changed = function () {
        $('#duration').html('');
        var reggie = /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/;
        var starts;
        var starts_array = reggie.exec($('#id_starts').val());
        if (starts_array) {
            starts = new Date(
                (+starts_array[1]),
                (+starts_array[2]) - 1, // Careful, month starts at 0!
                (+starts_array[3]),
                (+starts_array[4]),
                (+starts_array[5]),
                (+starts_array[6])
            );
        }
        else {
            starts = new Date($('#id_starts').val());
        }
        var ends;
        var ends_array = reggie.exec($('#id_ends').val());
        if (ends_array) {
            ends = new Date(
                (+ends_array[1]),
                (+ends_array[2]) - 1, // Careful, month starts at 0!
                (+ends_array[3]),
                (+ends_array[4]),
                (+ends_array[5]),
                (+ends_array[6])
            );
        }
        else {
            ends = new Date($('#id_ends').val());
        }
        if (!isFinite(starts) || !isFinite(ends))
            return;
        var duration = (days_between(starts, ends) + 1);
        if (duration < 1) {
            $('#duration').html('<span class="errorlist">End date can\'t be earlier than Start date</span>');
            return;
        }
        var plural = duration > 1 ? ' days' : ' day'
        $('#duration').html('[ ' + duration + plural + ' ]');
    }

    $('#id_starts').datepicker();
    $('#id_ends').datepicker();
    $('#id_starts').on('change', date_changed);
    $('#id_ends').on('change', date_changed);

    date_changed();

});

function FileVM(data) {
    var self = this;

    self.description = ko.observable();
    self.file = ko.observable();
    self.id = ko.observable(null);

    for (var i in data) {
        self[i] = ko.observable(data[i]);
    }
}


function FilesVM(data) {
    var self = this;

    self.files = ko.observableArray();
    self.deleted_rows = ko.observableArray();

    for (var i in data) {
        self.files.push(new FileVM(data[i]));
    }

    self.remove_row = function (row) {
        self.files.remove(row);
        if (row.id())
            self.deleted_rows.push(row.id());
    }

    self.add_row = function (row) {
        self.files.push(new FileVM({}));
    }

}


function ParticipantVM(data) {
    var self = this;
    for (var k in data) {
        self[k] = data[k];
    }
}

function TrainingVM() {

//    var $available = $('#available').selectize({
//        valueField: 'id',
//        labelField: 'name'
//    })[0].selectize;


    var self = this;


    self.selected_participant = ko.observable();

    $.ajax({
        url: '/training/participants.json',
        dataType: 'json',
        async: false,
        success: function (data) {
            self.all_participants = ko.observableArray(ko.utils.arrayMap(data, function (item) {
                return new ParticipantVM(item);
            }));
        }
    });

    self.selected_participants = ko.observableArray();
    self.participants = ko.observableArray();

    for (var k in participants) {
        var selected_item = $.grep(self.all_participants(), function (i) {
            return i.id == participants[k];
        })[0];
        self.selected_participants.push(selected_item);
        self.participants.push(parseInt(selected_item.id));
    }

    self.participants_available = ko.observableArray();

    self.refresh_participants = function () {
        for (var i = 0; i < self.all_participants().length; i++) {
            var exists = false;
            for (var j = 0; j < self.participants().length; j++) {
                if (self.all_participants()[i].id == self.participants()[j]) {
                    exists = true;
                    break;
                }
            }
            if (!exists) {
                self.participants_available.push(self.all_participants()[i]);
            }
            else {
            }
        }
    };
    self.refresh_participants();


    self.add_participant = function () {
        var selected_item = $.grep(self.all_participants(), function (i) {
            return i.id == self.selected_participant();
        })[0];
        self.participants.push(parseInt(self.selected_participant()));
        self.selected_participants.push(selected_item);
        self.participants_available.remove(selected_item);
        self.available.removeOption(self.selected_participant());
    }


    self.remove_row = function (row) {
        self.selected_participants.remove(row);
        self.participants_available.push(row);
        self.participants.remove(parseInt(row.id));
        self.available.addOption({
            text: row.name,
            value: row.id
        });
    }


    $('#add-participant form').submit(function (e) {
//        override_form(e, $(this), 'categories');
        var $form = $(this);
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),

            success: function (obj, status) {
//                $selectized[key].addOption({
//                    text: obj.name,
//                    value: obj.id
//                });
//                $selectized[key].addItem(obj.id);
                var new_participant = new ParticipantVM(obj);
                self.all_participants.push(new_participant);
                self.selected_participants.push(new_participant);
                self.participants.push(new_participant.id);
                $form.closest('.reveal-modal').foundation('reveal', 'close');
//                $categories.refreshItems();
            }
        });

        e.preventDefault();
    });


}
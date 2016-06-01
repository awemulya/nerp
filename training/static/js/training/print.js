$(document).ready(function () {

    var date_changed = function () {
        $('#duration').html('');
        var reggie = /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/;
        var starts;
        var starts_array = reggie.exec($('#id_starts').text());
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
            starts = new Date($('#id_starts').text());
        }
        var ends;
        var ends_array = reggie.exec($('#id_ends').text());
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
            ends = new Date($('#id_ends').text());
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

    date_changed();

    window.print();

});

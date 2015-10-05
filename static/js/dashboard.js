$(document).ready(function () {
    //when a group is shown, save it as the active accordion group
    $("#accordion").on('shown.bs.collapse', function () {
        var active = $("#accordion .in").attr('id');
        $.cookie('activeAccordionGroup', active);
        //  alert(active);
    });
    $("#accordion").on('hidden.bs.collapse', function () {
        $.removeCookie('activeAccordionGroup');
    });
    var last = $.cookie('activeAccordionGroup');
    if (last != null) {
        //remove default collapse settings
        $("#accordion .panel-collapse").removeClass('in');
        //show the account_last visible group
        $("#" + last).addClass("in");
    }
});
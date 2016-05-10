$(document).ready(function () {
	var $select = $('#id_authors, #id_subjects, #id_published_places').selectize({
        delimiter: ',',
        persist: false,
        create: function(input) {
            console.log(input);
            var re = /^[0-9]+$/;
            if (input.search(re) == -1){
                return {
                    value: input,
                    text: input
                }
            } else {
                return {
                    value: null,
                    text: null
                }
            };
        }
    });
    $('#id_languages').selectize({
    });
});
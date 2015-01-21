// Converts all starting letter of the string to Uppercase
function ucFirstAllWords( str )
{
    var pieces = str.split(" ");
    for ( var i = 0; i < pieces.length; i++ )
    {
        var j = pieces[i].charAt(0).toUpperCase();
        pieces[i] = j + pieces[i].substr(1);
    }
    return pieces.join(" ");
}

// This function gets the choices from api and updated observable
function getModelChoice(m_url, choice_field, value)
{
	var opt_list = [];
	    $.get(m_url, function(data)
	    {
		    for(i=0;i<data.length;i++)
		    {
			    var user = {
				    text: data[i][choice_field],
				    value: data[i].id
				};
			    opt_list.push(user);
		    };
		    
	    }).done(function(){
	    	value(opt_list);
	    });

}

ko.bindingHandlers.customSelectize = {
	init: function(element, valueAccessor, allBindings){
				var json_url = allBindings.get('modelUrl');
				var choice_field = allBindings.get('choiceField');
				var value = valueAccessor();
				// Updates the select options in an observable array
				getModelChoice(json_url, choice_field, value);
				var $select = $(element).selectize({
					plugins: ['remove_button'],
					});
				var z = ucFirstAllWords($(element)
      					.attr('name')
      					.replace(/_/g, ' '));
      			var element_to_append = $(element)
      					.parent()
      					.find('.selectize-dropdown.multi.plugin-remove_button');
      			var html_to_append = '<div class="custom-selectize-add-button" data-reveal-id="' + 
      							$(element).attr('name') +
      							'">Add '+ 
      						z +
      						'</div>';
      			// Add option appended to selectize
      			$(element_to_append).append(html_to_append);
				var selectizeControl = $select[0].selectize;
				
				// This event handler shows add option when all items are continiously selected
				selectizeControl.on('dropdown_close', function() {
					var parent = $(element)
      					.parent();
      				var ele = $(parent).find('.selectize-dropdown.multi.plugin-remove_button');
					var choice_ele = $(ele).find('.selectize-dropdown-content').find('.option');
					var choice_length = choice_ele.length;
					var is_focus = $(parent).find('.selectize-input.items').hasClass("focus");
					if(choice_length == 0 & is_focus){
						$(ele).css("display","block");
						}
					}
				);
				
				// This event handler shows Add option when item is full and select field is back in focus
				$(element).on('click', function() {
					var parent = $(element)
      					.parent();
      				var ele = $(parent).find('.selectize-dropdown.multi.plugin-remove_button');
					$(ele).css("display","block");
					}
				);
	},
	
	// This object shows observable value when changed. And also populate options when init updates it from api.
	update: function(element, valueAccessor, allbinding){
				var value = valueAccessor();
				var valueUnWrapped = ko.unwrap(value);
				var $select = $(element).selectize();
				var selectize = $select[0].selectize;
				for(i=0;i<valueUnWrapped.length;i++){
					selectize.addOption(valueUnWrapped[i]);
				};
				console.log(valueUnWrapped);
	},
};

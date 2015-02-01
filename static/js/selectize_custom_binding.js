
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
      					.next()
      					.find('.selectize-dropdown');
      			var html_to_append = '<div style="text-align:center;font-weight:bold;background-color:#0082bd;font-size:1em;padding:0.5em" data-reveal-id="' + 
      							$(element).attr('name') +
      							'">Add '+ 
      						z +
      						'</div>';
      			// Add option appended to selectize
      			$(element_to_append).append(html_to_append);
				var selectizeControl = $select[0].selectize;
				
				// This event handler shows add option when all items are continiously selected
				selectizeControl.on('dropdown_close', function() {
					var next = $(element)
      					.next();
      				var ele = $(next).find('.selectize-dropdown');
					var choice_ele = $(ele).find('.selectize-dropdown-content').find('.option');
					var choice_length = choice_ele.length;
					var is_focus = $(next).find('.selectize-input.items').hasClass("focus");
					if(choice_length == 0 & is_focus){
						$(ele).css("display","block");
						}
					}
				);
				
				// This event handler shows Add option when item is full and select field is back in focus
				$(element).next().find('.selectize-input.items').on('click', function() {
					console.log('this seemed to be clicked');
					var next = $(element)
      					.next();
      				var ele = $(next).find('.selectize-dropdown');
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

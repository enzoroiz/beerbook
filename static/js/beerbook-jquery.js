$(document).ready( function() {

    $("#rate-btn").click( function(event) {
        $( "#rate-popup" ).dialog({
			//width: 350,
            //height: 200,
            closeOnEscape: true,
            draggable: true,
			title: 'Add Rating!',
			
		});
    });
    
    $("#rate-btn-add").click( function(event) {
		
		var beerslug;
		var user;
		var rating;	
		
		beerslug = $(this).attr("data-beerslug");
		
		$.get('/beerbook/add_rating/', {beer_slug: beerslug});		
		
		
		$( "#rate-popup" ).dialog('close')
		});
    
    
    $("#rate-btn-cancel").click( function(event) {
		$( "#rate-popup" ).dialog('close')});
    
});

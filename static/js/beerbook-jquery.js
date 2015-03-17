$(document).ready( function() {

    $("#rate-btn").click( function(event) {
        $( "#rate-popup" ).dialog({
			width: 500,
            height: 275,
            closeOnEscape: true,
            draggable: true,
            resizable: false,
			title: 'Add Rating!',
			show: {effect: 'scale', duration: 200},
			hide: {effect: 'puff', duration: 200},
			dialogClass: 'rat',
			
		});
		//$(".rat .ui-dialog-title").css("font-size", "5px");
		$(".rat .ui-widget-content").css("background-color", "#F8F8F8");
		$(".rat .ui-widget-content").css("border", "5px solid #DD4814");
		//$(".rat .ui-dialog-titlebar").css("display", "none");
		$(".rat .ui-widget-content").css("padding", "0px");		
		$(".rat .ui-widget-header").css("color", "white");	
		//$(".rat .ui-widget-header").css("border", "none");		
		$(".rat .ui-dialog-titlebar").css("background", "#DD4814");		
		
    });
    
    $("#rate-btn-add").click( function(event) {
		
		var beerslug;
		var user;
		var rating;	
		
		beerslug = $(this).attr("data-beerslug");
		user = $(this).attr("data-user");
		rating = $("input[name='add-rating']:checked").val();
		
		$.get('/beerbook/add_rating/', {beer_slug: beerslug, username: user, rating_val: rating});		
		
		
		$( "#rate-popup" ).dialog('close')
		});
    
    
    $("#rate-btn-cancel").click( function(event) {
		$( "#rate-popup" ).dialog('close')});
		
	
});



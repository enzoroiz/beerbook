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
		var review;
		
		beerslug = $(this).attr("data-beerslug");
		user = $(this).attr("data-user");
		rating = $("input[name='add-rating']:checked").val();
		review = $("textarea[name='rate-text']").val();
		
		$.get('/beerbook/add_rating/', {beer_slug_val: beerslug, username_val: user, rating_val: rating, review_val: review},
										function(data){
																		
											$( "#no-rating" ).remove();											
											$( "#rev-list" ).prepend( "<div class=\"list-group-item\">" +
																		"<h4 class=\"list-group-item-heading\">\"" +
																		review +
																		"\"<br>- " + 
																		rating +
																		"/5</h4>" +
																		"<p align=\"right\" class=\"list-group-item-text\">-" +
																		user +
																		" - " + $.datepicker.formatDate('dd M yy' , new Date()) +
																		"</p></div>" );
											$( "#rate-btn" ).hide();
																		
											
											});
										
				
		
		
		$( "#rate-popup" ).dialog('close');
		
		});
    
    
    $("#rate-btn-cancel").click( function(event) {
		$( "#rate-popup" ).dialog('close')});
		
//	Edit profile
	$('#edit').click(function(){
		$.get('/beerbook/edit_profile/', {}, function(data){
			$('#edit_profile').html(data).ready(function(){
				$('#cancel').click(function(){
					location.reload()
				});
			});
		$('#profile_data').hide();
		});
	});

//	Change Password
	$('#change_password').click(function(){
		$.get('/beerbook/change_password/', {}, function(data){
			$('#change_password_div').html(data).ready(function(){
				$('#cancel_password').click(function(){
					location.reload()
				});
			});
		$('#profile_data').hide();
		});
	});

	$('#cancel_password').click(function() {
		window.location.replace(window.location.href);
	});
});



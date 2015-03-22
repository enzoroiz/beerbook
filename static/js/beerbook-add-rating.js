
$(function() {
$('#textDesc').keyup(function () {
		  var max = 255;
		  var len = $(this).val().length;
		  if (len >= max) {
			$('#charNum').text(' you have reached the limit');
		  } else {
			var char = max - len;
			$('#charNum').text('(' + char + ' characters left)');
		  }
	});
});




$(document).ready( function() {

    $("#rate-btn").click( function(event) {
        $( "#rate-popup" ).dialog({
			width: 400,
            height: 250,
            closeOnEscape: true,
            draggable: true,
            resizable: false,
			title: 'Add Rating!',
			show: {effect: 'scale', duration: 200},
			hide: {effect: 'puff', duration: 200},
			dialogClass: 'rating-pop',
			
		});
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
		
		$.get('/beerbook/add_rating/', {beer_slug_val: beerslug, rating_val: rating, review_val: review},
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
		



});

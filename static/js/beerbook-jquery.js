$(document).ready( function() {
	
		
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



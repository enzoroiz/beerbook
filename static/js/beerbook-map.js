$(document).ready( function() {

    $("#btn-map-open").click( function(event) {
        $( "#map-popup" ).dialog({
			
			// map basic attributes
			width: 800,
            height: 500,
            closeOnEscape: true,
            draggable: true,
            resizable: false,
			title: 'Beer Map!',
			//show: {effect: 'scale', duration: 200},
			//hide: {effect: 'puff', duration: 200},
			dialogClass: 'map',
			
		});
		
		// map styling
		$(".map .ui-widget-content").css("background-color", "#F8F8F8");
		$(".map .ui-widget-content").css("border", "5px solid #DD4814");		
		$(".map .ui-widget-content").css("padding", "0px");		
		$(".map .ui-widget-header").css("color", "white");				
		$(".map .ui-dialog-titlebar").css("background", "#DD4814");		
		
		//$(".rat .ui-widget-header").css("border", "none");
		//$(".map .ui-dialog-titlebar").css("display", "none");
		//$(".map .ui-dialog-title").css("font-size", "5px");
		
		
		// closes map
		$("#btn-map-close").click( function(event) {
			$( "#map-popup" ).dialog('close')});
		
    }); 

});

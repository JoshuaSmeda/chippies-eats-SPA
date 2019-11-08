$(document).ready(function() {
        console.log("JQuery Loaded");
	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				name : $('#user :selected').text(),
				menu : $('#menu :selected').text()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();
	});
});

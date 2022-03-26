<script>
	$( function() {

	$( "#Search" ).autocomplete({
	  source: "{% url 'UKCB:index' %}"
	});
	} );
</script>
	 
<script>
	function myMap() {
	var mapProp = {
	  center:new google.maps.LatLng(54.5,-4.5),
	  mapTypeId: google.maps.MapTypeId.ROADMAP,
	  zoom:5,
	};
	var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
	}
	var marker = new google.maps.Marker({position: center, map:map})
</script>
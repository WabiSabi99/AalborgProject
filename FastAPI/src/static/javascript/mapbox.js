api_token = "pk.eyJ1IjoiamFjb2JwaGlsbGlwc2RrIiwiYSI6ImNsNGc5a2htNDAxbnAzY3M3OTBsbnB2anMifQ.4QOcID_maHtm87qYW_oqHw"
mapboxgl.accessToken = api_token;


const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/jacobphillipsdk/cltxdr8u300e801qsg909ckgn', // style URL
  center: [9.9287, 57.0479], // starting position [lng, lat]
  zoom: 17, // starting zoo
});


// // Add zoom and rotation controls to the map.
// map.addControl(new mapboxgl.NavigationControl());



map.on('load', function() {
  map.addSource('single_point', {
    type: 'geojson',
    data: '/javascript/geodata/output.geojson' // Replace with the path to your local GeoJSON file
  });

  // Add a layer to render the point
  map.addLayer({
    id: 'Point',
    type: 'circle',
    source: 'single_point',
    paint: {
      'circle-radius': 6,
      'circle-color': 'red'
    }
  });
});



// Get the current zoom level
const zoom = map.getZoom();

// Get the current center of the map
const center = map.getCenter();

// Update the HTML elements with the new zoom level and center
document.getElementById('zoom').textContent = zoom.toFixed(2);
document.getElementById('lng').textContent = center.lng.toFixed(6);
document.getElementById('lat').textContent = center.lat.toFixed(6);




map.on('move', function() {
  // Get the current zoom level
  const zoom = map.getZoom();

// Get the current center of the map
  const center = map.getCenter();
  // Update the HTML elements with the new zoom level and center
  document.getElementById('zoom').textContent = zoom.toFixed(2);
  document.getElementById('lng').textContent = center.lng.toFixed(6);
  document.getElementById('lat').textContent = center.lat.toFixed(6);
});




map.on('zoomend', function() {
  // Get the current zoom level
  var zoom = map.getZoom();

  // Round the zoom level to the nearest integer
  var roundedZoom = Math.round(zoom);

  // Set the map's zoom level to the rounded value
  map.setZoom(roundedZoom);
});


// Disable the default scroll wheel zoom behavior
map.scrollZoom.disable();





// Add an event listener for the wheel event
map.getCanvas().addEventListener('wheel', function(e) {
  // Prevent the default behavior
  e.preventDefault();

  // Determine whether the wheel was scrolled up or down
  var delta = Math.sign(e.deltaY);

  // Get the current zoom level
  var zoom = map.getZoom();

  // If the wheel was scrolled up, increase the zoom level by 1
  // If the wheel was scrolled down, decrease the zoom level by 1
  var newZoom = zoom - delta;

  // Set the new zoom level
  map.setZoom(newZoom);
});


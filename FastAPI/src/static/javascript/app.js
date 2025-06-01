api_token = "pk.eyJ1IjoiamFjb2JwaGlsbGlwc2RrIiwiYSI6ImNsNGc5a2htNDAxbnAzY3M3OTBsbnB2anMifQ.4QOcID_maHtm87qYW_oqHw"
mapboxgl.accessToken = api_token;

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/jacobphillipsdk/cltxdr8u300e801qsg909ckgn', // style URL
    center: [9.9287, 57.0479], // starting position [lng, lat]
    zoom: 17, // starting zoo
});

// Get the current zoom level
const zoom = map.getZoom();
// Get the current center of the map
const center = map.getCenter();

// Update the HTML elements with the new zoom level and center
document.getElementById('zoom').textContent = zoom.toFixed(2);
document.getElementById('lng').textContent = center.lng.toFixed(6);
document.getElementById('lat').textContent = center.lat.toFixed(6);

map.on('move', function () {
    // Get the current zoom level
    const zoom = map.getZoom();

// Get the current center of the map
    const center = map.getCenter();
    // Update the HTML elements with the new zoom level and center
    document.getElementById('zoom').textContent = zoom.toFixed(2);
    document.getElementById('lng').textContent = center.lng.toFixed(6);
    document.getElementById('lat').textContent = center.lat.toFixed(6);
});


map.on('zoomend', function () {
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
map.getCanvas().addEventListener('wheel', function (e) {
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


// map.on('load', function () {
//     map.addSource('single_point', {
//         type: 'geojson',
//         data: 'path.geojson' // Replace with the path to your local GeoJSON file
//     });
//
//     // Add a layer to render the point
//     map.addLayer({
//         id: 'Point',
//         type: 'circle',
//         source: 'single_point',
//         paint: {
//             'circle-radius': 6,
//             'circle-color': 'red'
//         }
//     });
// });


// map.on('load', () => {
//     map.addSource('route', {
//         'type': 'geojson',
//         'data': {
//             'type': 'Feature',
//             'properties': {},
//             'geometry': {
//                 'type': 'LineString',
//                 'coordinates': [[9.9286385, 57.0481397], [9.9283466, 57.0482463], [9.9281912, 57.048081], [9.92814, 57.0480266], [9.9280897, 57.0479711], [9.9280367, 57.0479134], [9.9278702, 57.0478496], [9.9276838, 57.0476821], [9.9275231, 57.0476388], [9.9273366, 57.0474728], [9.9272885, 57.0474317], [9.9272609, 57.0474055], [9.9272214, 57.0473884], [9.927172, 57.0473737], [9.9270418, 57.0473663], [9.9269409, 57.0473839], [9.926924, 57.0473864], [9.9269097, 57.0473889], [9.926821, 57.0474041], [9.9263648, 57.0474821], [9.9259619, 57.0475511], [9.9257303, 57.0475907], [9.9257015, 57.0475573], [9.9256556, 57.0474799], [9.9253608, 57.0469892], [9.9251816, 57.0466776], [9.9251217, 57.0466745], [9.9245026, 57.0467404], [9.9242175, 57.0467635], [9.92414, 57.0467701], [9.9240945, 57.0467715], [9.923793, 57.0468172], [9.9235111, 57.046863], [9.9233507, 57.0468901], [9.9232997, 57.0469065], [9.9232898, 57.0468744], [9.9230896, 57.0469146], [9.9225043, 57.047032], [9.9219576, 57.0471517], [9.921354, 57.047296], [9.9212359, 57.0473239], [9.920698, 57.0474551], [9.920597, 57.0474964], [9.9201987, 57.0475571], [9.9200468, 57.0475811], [9.9198435, 57.0476122], [9.9195816, 57.047657], [9.9193422, 57.0477067], [9.9192703, 57.0477199], [9.9191372, 57.0477474], [9.9189653, 57.0477821], [9.918814, 57.0478086], [9.9186962, 57.0478246], [9.9186361, 57.0478315], [9.9182692, 57.0479244], [9.9182406, 57.0479794], [9.9179717, 57.0480123], [9.9175734, 57.0480838], [9.9172927, 57.0481754], [9.9171756, 57.0482042], [9.9166401, 57.0482884], [9.9160734, 57.0483411], [9.9159178, 57.0483553], [9.9158662, 57.04836], [9.9158324, 57.0482989], [9.9157744, 57.0482225], [9.9155461, 57.0480122], [9.9154605, 57.0479099], [9.915372, 57.0478062], [9.9151449, 57.0475847], [9.915109, 57.0475129], [9.9150464, 57.0474527], [9.9147756, 57.0472228], [9.9147208, 57.0471777], [9.9146565, 57.0471249], [9.9145806, 57.0470625], [9.9142677, 57.0469012], [9.9142274, 57.0468726], [9.9140704, 57.0467648], [9.9139401, 57.0466847], [9.9138277, 57.0466198], [9.9137058, 57.0465581], [9.9136356, 57.0465164], [9.9135685, 57.0464735], [9.9135342, 57.0464136], [9.9135095, 57.0463751], [9.9134038, 57.0462653], [9.9133719, 57.0462305], [9.9131649, 57.0459997], [9.9129106, 57.0457142], [9.9127259, 57.0454891], [9.9126314, 57.0453631], [9.9122679, 57.0448111], [9.9122305, 57.0447549], [9.9121717, 57.0446665], [9.9120893, 57.044541], [9.9120521, 57.0444843], [9.9116174, 57.043816], [9.9118047, 57.0437803], [9.9117646, 57.0437237], [9.9118036, 57.043713], [9.9115628, 57.0433639], [9.9115639, 57.0433423], [9.9115849, 57.0433272], [9.9115271, 57.0432409], [9.9114353, 57.0431025], [9.9113195, 57.0430145], [9.9111945, 57.0425357], [9.9111837, 57.0424754], [9.9110567, 57.0424826]]
//
//             }
//         }
//     });
//     map.addLayer({
//         'id': 'route',
//         'type': 'line',
//         'source': 'route',
//         'layout': {
//             'line-join': 'round',
//             'line-cap': 'round'
//         },
//         'paint': {
//             'line-color': '#888',
//             'line-width': 8
//         }
//     });
// });


document.addEventListener('DOMContentLoaded', function () {
    const runButton = document.getElementById('run-button');
    runButton.addEventListener('click', get_start_and_goal);

    function get_start_and_goal() {
        const startPos = document.getElementById('startPos').value;
        const endPos = document.getElementById('endPos').value;

        console.log('Button clicked!');
        console.log(startPos);
        console.log(endPos);

        // Split the startpos and endpos based on comma
        var start_x = parseFloat(startPos.split(',')[0]);
        var start_y = parseFloat(startPos.split(',')[1]);
        var end_x = parseFloat(endPos.split(',')[0]);
        var end_y = parseFloat(endPos.split(',')[1]);

        // Construct the data to send
        const data = {
            "startPos": {"x": start_x, "y": start_y},
            "endPos": {"x": end_x, "y": end_y}
        };
        send_http_request('http://localhost:8000/api/get_path', data);
    }

    let routeLayerAdded = false; // Variable to track whether the route layer is added

    function send_http_request(url, data) {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        fetch(url, {
            method: 'POST',
            headers: myHeaders,
            body: JSON.stringify(data),
            redirect: 'follow'
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(result => {
                console.log('Fetch operation successful');
                console.log('Received path coordinates:', result);

                // Remove existing layer and source if they exist
                if (map.getSource('route')) {
                    map.removeLayer('route');
                    map.removeSource('route');
                }

                // Add a delay before adding the new layer
                setTimeout(() => {
                    // Add the new source and layer to the map
                    map.addSource('route', {
                        'type': 'geojson',
                        'data': {
                            'type': 'Feature',
                            'properties': {},
                            'geometry': {
                                'type': 'LineString',
                                'coordinates': result,
                            }
                        }
                    });
                    map.addLayer({
                        'id': 'route',
                        'type': 'line',
                        'source': 'route',
                        'layout': {
                            'line-join': 'round',
                            'line-cap': 'round'
                        },
                        'paint': {
                            'line-color': 'red',
                            'line-width': 8
                        }
                    });
                }, 500); // Adjust the delay time (in milliseconds) as needed
            })
            .catch(error => {
                console.error('There was a problem with your fetch operation:', error);
            });
    }

});










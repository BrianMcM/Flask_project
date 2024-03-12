// Initialize and add the map
let map;

//async load JSON static data
 async function loadJSON() {
  try {
      const response = await fetch('/get_static_data');
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log("Test console log")
      const bikeStations = [];
      for (let key in data) {
          const position = [{ lat: parseFloat(data[key].position_lat), lng: parseFloat(data[key].position_lng)}, data[key].name ];
          bikeStations.push(position);
      }

      return bikeStations;
  } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      // If an error occurs, you might want to return a default value or handle it in some way
      return [];
  }
}

//async load JSON static data
async function loadstationJSON(station_number) {
  try {
    console.log('/get_station_occupancy/'+station_number)
    const response = await fetch('/get_station_occupancy/'+station_number);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    const data = await response.json();
    console.log(data)
    const bikeStations = [];

    return bikeStations;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    // If an error occurs, return a default empty array
    return [];
  }
}

async function initMap() {
  loadstationJSON(5);
  // The location of center of map (The Spire)
  const center_dublin = { lat: 53.35026632919465, lng: -6.260428242778603 }; 
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");

  // The map, centered at The Spire
  map = new Map(document.getElementById("map"), {
    zoom: 13,
    center: center_dublin,
    mapId: "992d9c838bb18c39",
  });

  // info windows for markers
 // Create an info window to share between markers.

 //call loadJSON function which is static data, then create the markers based on that data
loadJSON()
    .then(bikeStations => {

// Create an info window to share between markers.
const infoWindow = new google.maps.InfoWindow();
const infoBox = document.getElementById('info-box');

// Create the markers.

bikeStations.forEach(([position, title], i) => {
  const marker = new google.maps.Marker({
    position,
    map:map,
    title: `${i + 1}. ${title}`,
    optimized: false,
    icon: {
      url: "../static/images/bicycle-bike.svg",
      scaledSize:new google.maps.Size(50,50)
    }
  });

  // Add a click listener for each marker, and set up the info window.
  marker.addListener("click", () => {
    infoWindow.close();
    infoWindow.setContent(marker.getTitle());
    infoWindow.open(marker.getMap(), marker);
  });

  marker.addListener('click', () => {
    infoBox.innerHTML = '<h2>Marker Information</h2>' +
                        '<p>Marker Name: ' + marker.getTitle() + '</p>' +
                        '<p>Location: Latitude ' + marker.getPosition().lat() + ', Longitude ' + marker.getPosition().lng() + '</p>';
});
});

})
.catch(error => {
    console.error('Error loading JSON:', error);
});
}

initMap();

var map;
var datasource, popup, pandaSymbolLayer, cameraSymbolLayer, heatmap_layer, cameras

async function retrieveIconData(){
  const camera_list_response = await fetch(`/getCameraList`)
  const cameras_locations = await camera_list_response.json();

  const sightings_response = await fetch(`/getSightings`)
  const panda_sightings = await sightings_response.json();

  return [cameras_locations, panda_sightings]
}

async function GetMap() {
    response = await retrieveIconData()
    camera_locations = response[0]["camera_list"]
    cameras = []

    panda_sightings = response[1]["sightings_list"]
    //Initialize a map instance.
    map = new atlas.Map('myMap', {
    center: [85.331,27.72],
    zoom: 8,
    view: 'Auto',
    style: 'night',

        //Add authentication details for connecting to Azure Maps.
        authOptions: {
        authType: 'subscriptionKey',
        subscriptionKey: '#enter your subscription key here'
    }
    });

    //Wait until the map resources are ready.
    map.events.add('ready', function () {

      map.controls.add(new atlas.control.StyleControl({
        mapStyles: ['road', 'grayscale_dark', 'night', 'road_shaded_relief', 'satellite', 'satellite_road_labels']
      }), {
        position: 'top-right'
      });  
        
        //Create a data source and add it to the map.
        camera_datasource = new atlas.source.DataSource(null, {
            cluster: true
        });

        panda_datasource = new atlas.source.DataSource(null, {
          cluster: true,

          //The radius in pixels to cluster points together.
          clusterRadius: 100
        });

        map.sources.add(camera_datasource);
        map.sources.add(panda_datasource);

        // var panda_img = "https://redpanda.blob.core.windows.net/other/logo.png"
        var panda_img = "https://raw.githubusercontent.com/faridelaouadi/LeetCode/master/red_panda-removebg-preview.png"
        var camera_img = 'https://cdn.iconscout.com/icon/free/png-512/apple-camera-493147.png'
        
        map.imageSprite.add('camera_icon', camera_img)
        map.imageSprite.add('panda_icon', panda_img)


        //Create three point features on the map and add some metadata in the properties which we will want to display in a popup.
        camera_location_list = []
        //console.log("WE ARE PRINTING THE CAMERA LOCATIONS")
        for (camera in camera_locations){
          //console.log(camera_locations[camera])
          var new_camera = new atlas.data.Feature(new atlas.data.Point([camera_locations[camera][1],camera_locations[camera][2]]), {modalLink:'#cameraModal', cameraID: camera_locations[camera][0], category:"camera"});
          cameras.push(camera_locations[camera][0])
          camera_location_list.push(new_camera)
        }
        // var camera1 = new atlas.data.Feature(new atlas.data.Point([85.331,27.72]), {modalLink:'#cameraModal', cameraID: '0010', category:"camera"});
        // var camera2 = new atlas.data.Feature(new atlas.data.Point([86.331,27.72]), {modalLink:'#cameraModal', cameraID: '0011', category:"camera"});
        // var camera3 = new atlas.data.Feature(new atlas.data.Point([85.331,28.12]), {modalLink:'#cameraModal', cameraID: '0012', category:"camera"});
        // var camera4 = new atlas.data.Feature(new atlas.data.Point([84.331,27.72]), {modalLink:'#cameraModal', cameraID: '0013', category:"camera"});

        panda_sightings_list = []
        for (panda_sighting in panda_sightings){
          //console.log(camera_locations[camera])
          var new_panda = new atlas.data.Feature(new atlas.data.Point([panda_sightings[panda_sighting][1],panda_sightings[panda_sighting][2]]), {modalLink:'#pandaModal', imageURL: panda_sightings[panda_sighting][0], category:"panda"});
          panda_sightings_list.push(new_panda)
        }
        //pandas next to camera 1
        // var panda1 = new atlas.data.Feature(new atlas.data.Point([85.331,27.52]), {category:"panda"});
        // var panda2 = new atlas.data.Feature(new atlas.data.Point([85.431,27.32]), {category:"panda"});
        // var panda3 = new atlas.data.Feature(new atlas.data.Point([85.531,27.62]), {category:"panda"});
        // var panda4 = new atlas.data.Feature(new atlas.data.Point([85.431,27.72]), {category:"panda"});

        // //pandas next to camera 2
        // var panda5 = new atlas.data.Feature(new atlas.data.Point([86.331,27.22]), {category:"panda"});
        // var panda6 = new atlas.data.Feature(new atlas.data.Point([86.421,27.62]), {category:"panda"});
        // var panda7 = new atlas.data.Feature(new atlas.data.Point([86.561,27.32]), {category:"panda"});
        // var panda8 = new atlas.data.Feature(new atlas.data.Point([86.611,27.72]), {category:"panda"});

        // //pandas next to camera 3
        // var panda9 = new atlas.data.Feature(new atlas.data.Point([85.231,28.12]), {category:"panda"});
        // var panda10 = new atlas.data.Feature(new atlas.data.Point([85.421,28.12]), {category:"panda"});
        // var panda11 = new atlas.data.Feature(new atlas.data.Point([85.561,28.12]), {category:"panda"});
        // var panda12 = new atlas.data.Feature(new atlas.data.Point([85.611,28.12]), {category:"panda"});

        // //pandas next to camera 4
        // var panda9 = new atlas.data.Feature(new atlas.data.Point([84.391,27.72]), {category:"panda"});
        // var panda10 = new atlas.data.Feature(new atlas.data.Point([84.331,27.79]), {category:"panda"});
        // var panda11 = new atlas.data.Feature(new atlas.data.Point([84.271,27.72]), {category:"panda"});
        // var panda12 = new atlas.data.Feature(new atlas.data.Point([84.331,27.68]), {category:"panda"});


        camera_datasource.add(camera_location_list);
        //Basically adding the image to the points
        cameraSymbolLayer = new atlas.layer.SymbolLayer(camera_datasource, null, {
            iconOptions: {
            image: 'camera_icon',
            size: 0.1
            },
            textOptions: {
                    //Convert the temperature property of each feature into a string and concatenate "°F".
                    textField: ['concat',  "Camera ID :", ['to-string', ['get', 'cameraID']]],
                    font: [
                        "SegoeFrutigerHelveticaMYingHei-Bold"
                      ],

                    //Offset the text so that it appears on top of the icon.
                    offset: [0, -3.9]
                }
        });

        panda_datasource.add(panda_sightings_list);
        pandaSymbolLayer = new atlas.layer.SymbolLayer(panda_datasource, null, {
            iconOptions: {
            image: 'panda_icon',
            size: 0.2
            },
        });

        heatmap_layer = new atlas.layer.HeatMapLayer(panda_datasource, null, {
          //Set the weight to the point_count property of the data points.
          weight: ['get', 'point_count'],

          //Optionally adjust the radius of each heat point.
          radius: 40
      }), 'labels'

        map.layers.add(heatmap_layer);

        
        map.layers.add(pandaSymbolLayer);
        map.layers.add(cameraSymbolLayer);

        //Add a click event to the symbol layer.
        map.events.add('click', cameraSymbolLayer, function (e) {
            //Get custom properties on the marker
            var properties = e.shapes[0].getProperties();
            console.log(properties)
            $('#cameraModalTitle').html("Camera ID : " + properties.cameraID);
            
            fetch(`/camera_images/${properties.cameraID}`)
            .then(function (response) {
                return response.text();
            }).then(function (text) {
                if (JSON.parse(text)['success']){
                  var urls = JSON.parse(text)['urls']
                  $('#total-pics-list').html("Total pics : " + urls.length);
                  var number_of_pandas = 0;
                  var number_of_non_pandas = 0;
                  for (imageURL in urls){
                    if (imageURL == 0){
                      $('#total-pics .carousel-inner').append(`<div class='carousel-item active'> <img src='${urls[imageURL][0]}' class='d-block w-100'></div>`)
                    }else{
                      $('#total-pics .carousel-inner').append(`<div class='carousel-item'> <img src='${urls[imageURL][0]}' class='d-block w-100'></div>`)
                    }
                    if (urls[imageURL][1]){
                      if (number_of_pandas == 0){
                        $('#panda-pics .carousel-inner').append(`<div class='carousel-item active'> <img src='${urls[imageURL][0]}' class='d-block w-100'></div>`)
                      }else{
                        $('#panda-pics .carousel-inner').append(`<div class='carousel-item'> <img src='${urls[imageURL][0]}' class='d-block w-100'></div>`)
                      }
                      number_of_pandas += 1
                      
                    }else{
                      if (number_of_non_pandas == 0){
                        $('#non-panda-pics .carousel-inner').append(`<div class='carousel-item active'> <img src='${urls[imageURL][0]}' class='d-block w-100'></div>`)
                      }else{
                        $('#non-panda-pics .carousel-inner').append(`<div class='carousel-item'> <img src='${urls[imageURL][0]}' class='d-block w-100'></div>`)
                      }
                      number_of_non_pandas += 1
                    }
                  }
                  $('#panda-pics-list').html("Total Pandas Spotted : " + number_of_pandas);
                  $('#non-panda-pics-list').html("False Positives : " + number_of_non_pandas);
                  $(properties.modalLink).modal('show')
                }else{
                  alert("No images found!")
                }
                
                //console.log(urls[imageURL])
                
                
            });
            
        });

        //Add a click event to the symbol layer.
        map.events.add('click', pandaSymbolLayer, function (e) {
          //Get custom properties on the marker
          var properties = e.shapes[0].getProperties();
          console.log(properties["imageURL"])
          $('#pandaImagePreview').attr('src', properties["imageURL"]);
          $(properties.modalLink).modal('show')
      });


        });
    }

    function filterSymbols(elm, cameraID) {
      //Set the visibility of the layer.
      console.log("we are filtering")
      console.log(cameraID)
      if (elm.checked) {
          //Add the category to the categories array.
          cameras.push(cameraID);
      } else {
          //Remove the category to the categories array.
          cameras.splice(cameras.indexOf(cameraID), 1);
      }

      //Create a filter that grabs the category of each point and checks that it is in the array of categories.
      var filter = ['in', ['get', 'cameraID'], ['literal', cameras]];

      //Update the filter in the layer.
      cameraSymbolLayer.setOptions({
          filter: filter
      });

  }


window.addEventListener("load", GetMap);

$(function() {
    "use strict";
     
	 
//sidebar menu js
$.sidebarMenu($('.sidebar-menu'));

// === toggle-menu js
$(".toggle-menu").on("click", function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });	 
	   
// === sidebar menu activation js

$(function() {
        for (var i = window.location, o = $(".sidebar-menu a").filter(function() {
            return this.href == i;
        }).addClass("active").parent().addClass("active"); ;) {
            if (!o.is("li")) break;
            o = o.parent().addClass("in").parent().addClass("active");
        }
    }), 	   
	   

/* Top Header */

$(document).ready(function(){ 
    $(window).on("scroll", function(){ 
        if ($(this).scrollTop() > 60) { 
            $('.topbar-nav .navbar').addClass('bg-dark'); 
        } else { 
            $('.topbar-nav .navbar').removeClass('bg-dark'); 
        } 
    });

 });


	    
   
$(function () {
  $('[data-toggle="popover"]').popover()
})


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


});


function loading(){
  $("#loading").show();
  $("#wrapper").hide();       
}

$('#cameraModal').on('hidden.bs.modal', function () {
  //clear the body so we can reuse it
  $('#total-pics .carousel-inner').html('');
  $('#panda-pics .carousel-inner').html('');
  $('#non-panda-pics .carousel-inner').html('');
});

function validateAddCameraForm(camera_list){
  var proposed_camera_ID = $("#proposedCameraID").val();
  current_cameras = []
  for (camera in camera_list){
    current_cameras.push(camera_list[camera][0])
  }
  if (current_cameras.includes(proposed_camera_ID)){
    alert("Value already exists for camera ID");
    return false
    
  }else{
    //alert(`Current cameras : ${current_cameras} and my proposed id is ${proposed_camera_ID}`)
    return True
  }

}


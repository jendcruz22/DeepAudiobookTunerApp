$(document).ready(function(){
    setTimeout(function(){
     $("#preloader").delay(6500).removeClass("animation").addClass("over");
     $(".pre-overlay").css({"height" : "0%"});
    }, 40000);
   });
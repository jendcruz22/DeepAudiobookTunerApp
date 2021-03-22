$(document).ready(function(){
    setTimeout(function(){
     $("#preloader").delay(650).removeClass("animation").addClass("over");
     $(".pre-overlay").css({"height" : "0%"});
    }, 4000);
   });
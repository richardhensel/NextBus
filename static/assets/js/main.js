// Parallax script 
$(function(){
  // cache the window object
  var $window = $(window);
  // parallax background effect
  $('section[data-type="background"]').each(function(){
    var $bgobj = $(this); //this is assigning the object
    $(window).scroll(function() {
      // scroll the background at var speed
      // the yPos is a -ve value since we are scrolling it up
      var yPos = -($window.scrollTop() / $bgobj.data('speed'));
      // put together our final background position 
      var coords = '50% ' + yPos + 'px';
      // move the background
      $bgobj.css({ backgroundPosition: coords });
    }); // end window scroll
  });
});


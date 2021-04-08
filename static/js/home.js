 /* NAVBAR */
 $('.nav-toggle').on('click', function (e) {
  $(this).toggleClass('nav-open');
  $(".menu").toggleClass("active");
});

/*LOGIN/SIGNUP ANIMATION */
$(document).ready(function(){
  $('.signupbox').css('transform', 'translateX(80%)');
  $('.signinbox').css('transform', 'translateX(0%)');
});

/*PROJECT TABS */
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }

  // Get the element with id="defaultOpen" and click on it
  document.getElementById("defaultOpen").click();
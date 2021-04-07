 /* NAVBAR */
 $('.nav-toggle').on('click', function (e) {
  $(this).toggleClass('nav-open');
  $(".menu").toggleClass("active");
});

/* APP OF THE DAY */
$(function () {
  $('.food > .info > .content .stars')
      .bind('mousemove', function (e) {
          var pct = e.pageX - $(this).offset().left;
          pct = pct / $(this).width() * 100;
          $(this).find('> em').css('width', pct + '%');
      })
      .bind('mouseleave', function () {
          $(this).find('> em').animate({
              width: '91%'
          }, 250);
      });
});

function showRateForm(){
    $("#rate-form").show();
}

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
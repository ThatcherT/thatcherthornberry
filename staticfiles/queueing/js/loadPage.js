// check if following DJ
followingDJ = jQuery.data(document.body, "followingDJ");
// check if I am a DJ
IAmDJ = jQuery.data(document.body, "IAmDJ");

function loadPage() {
  if (followingDJ || IAmDJ) {
    const bottomBar = document.getElementById("bottom-bar");
    bottomBar.style.display = "";
    if (IAmDJ) {
      loadProfilePage();
    } else {
      loadDJPage();
    }
  } else {
    mainContent.innerHTML = welcomeMsg;
    document.getElementById("get-started").style.display = "";
  }
}

var welcomeMsg = `<div class="row">
  <div class="col-12">
    <p>
      QSongs allows you to queue songs on your friends' devices. Or, become the
      DJ, and enable others to queue songs on your device.
    </p>
  </div>
</div>`;

loadPage();

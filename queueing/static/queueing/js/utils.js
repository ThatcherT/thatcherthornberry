/*
This document contains some helpful utils for shuffling, following, and queueing, loadpage, other.
*/

followingDJ = jQuery.data(document.body, "followingDJ")
IAmDJ = jQuery.data(document.body, "IAmDJ")
console.log(IAMDJ, followingDJ);
// STARTUP SCRIPT RUNS EVERY TIME!!!!!
loadPage();

function loadPage() {
  // check if any DJ relations exist
  if ( followingDJ || IAmDJ) {
    const bottomBar = document.getElementById("bottom-bar");
    bottomBar.style.display = "";
    if (IAmDJ) {
      loadProfilePage();
    } else {
      loadDJPage();
    }
  } else {
    loadWelcomePage();
  }
}


// send ajax to server and shuffle for IAmDJ
function shuffle() {
  $.ajax({
    url: "/ajax/shuffle/",
    data: {
      IAmDJ: IAmDJ,
      csrfmiddlewaretoken: window.CSRF_TOKEN,
    },
    type: "POST",
    dataType: "json",
    success: function (data) {
      // shuffle success message
      document.getElementById("shuffle-message").style.display = "";
      document.getElementById("shuffle-message").style.color = "green";
      document.getElementById("shuffle-message").innerHTML = "Shuffled!";
    },
    error: function (xhr, status, error) {
      // shuffle error message
      document.getElementById("shuffle-message").style.display = "";
      document.getElementById("shuffle-message").style.color = "red";
      document.getElementById("shuffle-message").innerHTML = "Some error.. sorry";
    },
  });
}

function followDJ() {
  // store dj in session
  const followingDJ = document.getElementById("follow-dj").value;
  $.ajax({
    url: "/ajax/follow-dj/",
    type: "POST",
    data: {
      csrfmiddlewaretoken: window.CSRF_TOKEN,
      followingDJ: followingDJ,
    },
    dataType: "json",
    success: function (data) {
      // update jQuery data
      loadPage();

      return true;
    },
    error: function (xhr, status, error) {
      alert(xhr.responseText);
      console.log(status, error);
      return false;
    },
  });
}

// send an ajax request with local storage data and data from an input element
function queue() {
  // get dj from session
  const song = document.getElementById("queue-song-input").value;
  $.ajax({
    url: "/ajax/queue/",
    type: "POST",
    data: {
      csrfmiddlewaretoken: window.CSRF_TOKEN,
      song: song,
      dj: followingDJ,
    },
    success: function (data) {
      return data.msg;
    }
  });
}

// handy util for updating the active icon
function updateActiveIcon(icon) {
  document.querySelectorAll(".bottom-bar .nav-icon").forEach(function (icon) {
    icon.classList.remove("active");
  });
  icon.classList.add("active");
}


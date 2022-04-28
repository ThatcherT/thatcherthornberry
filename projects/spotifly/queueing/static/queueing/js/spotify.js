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
      jQuery.data(document.body, "followingDJ", followingDJ);
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

function queue() {
  console.log("queue");
  // get dj from session
  const followingDJ = jQuery.data(document.body, "followingDJ");
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
      return true;
    }
  });
}
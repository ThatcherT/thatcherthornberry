// get the djs available by requesting the server
async function getDJs() {
  return $.ajax({
    url: "/ajax/get-djs/",
    type: "GET",
    data: {
      csrfmiddlewaretoken: window.CSRF_TOKEN,
    },
    dataType: "json",
    success: function (data) {
      return data;
    },
    error: function (xhr, status, error) {
      alert(xhr.responseText);
      console.log(status, error);
    },
  });
}

// return the HTML for the list of queued songs
function getQueueHTML() {
  let rowsHTML = "";
  // use jquery to get "queueMgmt"
  let queueMgmt = $("body").data("queueMgmt");
  if (Object.keys(queueMgmt.on_deck).length > 0) {
    rowsHTML += `<div class="row">
        <div class="col">
            On Deck
        </div>
    </div>`;
    // queueMgmt.on_deck is a dictionary where the key is a song's unique URI
    // and the value is the song object
    for (let songURI in queueMgmt.on_deck) {
      let songObj = queueMgmt.on_deck[songURI].song_object;
      rowsHTML += getSongRowHTML(songObj).outerHTML;
    }

    if (Object.keys(queueMgmt.queue).length > 0) {
      rowsHTML += `<div class="row">
        <div class="col">
            Queue
        </div>
    </div>`;
      // queueMgmt.queue is a dictionary where each key is a song's unique URI
      // it has a value of a dict with a key song_object
      // the value of the key song_object should be passed to getSongRowHTML
      for (let songURI in queueMgmt.queue) {
        let song = queueMgmt.queue[songURI].song_object;
        // TODO: this is pretty jank, no?
        rowsHTML += getSongRowHTML(song).outerHTML;
      }
    } else {
      rowsHTML += `<div class="row">
            <div class="col-12">
                <h2>No songs in queue</h2>
            </div>
        </div>`;
    }
  } else {
    rowsHTML += `<div class="row">
            <div class="col">
                <h2>For managed queue, DJ needs to start a Session</h2>
            </div>
        </div>`;
  }
  return rowsHTML;
}

async function getNowPlayingSongHTML() {
  let songData = await getNowPlaying();
  let rowHTML;
  if (songData.songObj) {
    rowHTML = getSongRowHTML(songData.songObj).outerHTML;
  } else {
    rowHTML = `<div class="row">
            <div class="col-12">
                <h2>No song playing</h2>
            </div>
        </div>`;
  }
  return rowHTML;
}

// DJ Page
async function loadDJPage() {
  // TODO: refactor this to be fast
  queueManagement();
  updateActiveIcon(document.getElementById("dj-icon"));
  if (getFollowingDJ()) {
    mainContent.innerHTML = `
              <div class="row">
                  <div class="col-12">
                      <p>
                          You are following ${getFollowingDJ()}
                      </p>
                  </div>
              </div>
              <div class="row">
                    <div class="col-12">
                        <button class="btn big-ole-btn btn-warning" onclick="unfollowDJ()">Unfollow</button>
                    </div>
                </div>
                <div class="row">
                    <div class="col-12">
                        <button id="copy-invite-link" class="btn btn-primary btn-lg big-ole-btn" onClick="copyInviteToClipboard('Follow')">
                            Copy Invite Link
                        </button>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        Now Playing
                    </div>
                </div>
                ${await getNowPlayingSongHTML()}
                ${getQueueHTML()}
              `;
  } else {
    const djObj = await getDJs();
    mainContent.innerHTML = `
            <div class="row">
                <div class="col-12">
                    <h1>Follow a DJ to Queue Songs.</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <select id="dj-select" class="selectpicker" data-style="btn-lg big-ole-btn" data-size="10" data-live-search="true">
                        <option selected disabled>Select a DJ</option>
                        ${djObj.djs
                          .map((dj) => `<option value="${dj}">${dj}</option>`)
                          .join("")}
                    </select>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <button id="follow-dj-btn" class="btn btn-primary btn-lg form-submit big-ole-btn" onClick="followDJ()">
                        Submit
                    </button>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <p id="follow-dj-error" class="error-message"></p>
                </div>
            </div>`;
    $("#dj-select").selectpicker().selectpicker("refresh");
  }
}

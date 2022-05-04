// Profile Page
function loadProfilePage() {
    updateActiveIcon(document.getElementById("profile-icon"));
    if (getIAmDJ()) {
      mainContent.innerHTML = `
              <div class="row">
                  <div class="col-12">
                      <h1>Profile</h1>
                  </div>
              </div>
              <div class="row">
                  <div class="col-12">
                      <p>
                          This is your profile.
                      </p>
                      <p>
                          You are DJ ${getIAmDJ()}
                      </p>
                      <button class="btn btn-primary big-ole-btn" onclick="shuffle()">Shuffle</button>
                  </div>
                  <! -- TODO REMOVE THIS -->
                  <div class="col-12">
                      <a href="https://accounts.spotify.com/authorize?client_id=81a9b3f937fc4430a1cf42210e2439bb&response_type=code&redirect_uri=http://127.0.0.1:8000/redirect&scope=user-read-private user-read-email user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-recently-played">
                        <button id="connect-with-spotify" class="btn btn-primary btn-lg big-ole-btn" style="background-color: green;">
                            Connect with Spotify
                        </button>
                      </a>
                  </div>
              </div>
              <div class="row">
                    <div class="col-12">
                        <button id="copy-invite-link" class="btn btn-primary btn-lg big-ole-btn" onClick="copyInviteToClipboard()">
                            Copy Invite Link
                        </button>
                    </div>
              </div>
              <div class="row">
                  <div class="col-12">
                      <p id="profile-page-message" style="padding-top: 10%;"></p>
                  </div>
              </div>`;
    } else {
      $.ajax({
        url: "/spotify/connect-link/",
        type: "GET",
        dataType: "json",
        data: {
          csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        success: function (data) {
          mainContent.innerHTML = `
              <div class="row">
                  <div class="col-12">
                      <h1>Connect with spotify to become a DJ</h1>
                  </div>
              </div>
              <div class="row">
                  <div class="col-12">
                      <a href="${data.url}">
                        <button id="connect-with-spotify" class="btn btn-primary btn-lg big-ole-btn" style="background-color: green;">
                            Connect with Spotify
                        </button>
                      </a>
                  </div>
              </div>`;
        },
        error: function (xhr, status, error) {
          alert(xhr.responseText);
        },
      });
    }
  }
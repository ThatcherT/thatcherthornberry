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
                      </p>`;

    if (getAnon()) {
      mainContent.innerHTML += `
            <p style='padding-top: 90px'>
                To complete sign up, send me the email you use for Spotify.
            </p>`;
    } else {
      mainContent.innerHTML += `<button class="btn btn-primary big-ole-btn" onclick="shuffle()">Shuffle</button>
                      <button class="btn btn-primary big-ole-btn" onclick="session()">Start Session</button>
                      <button class="btn btn-primary big-ole-btn" onclick="session(true)">Stop Session</button>
                  </div>
              </div>
              <div class="row">
                    <div class="col">
                        <button id="copy-invite-link" class="btn btn-primary btn-lg big-ole-btn" onClick="copyInviteToClipboard()">
                            Copy Invite Link
                        </button>
                    </div>
                    <div class="col">
                        <button id="log-out" class="btn btn-danger btn-lg big-ole-btn" onClick="logOut()">
                            Log Out
                        </button>
                    </div>
              </div>
              <div class="row" id="profile-playlists">
              </div>
              <div class="row">
                  <div class="col-12">
                      <p id="profile-page-message" style="padding-top: 10%;"></p>
                  </div>
              </div>`;
      getPlaylists();
    }
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
    });
  }
}

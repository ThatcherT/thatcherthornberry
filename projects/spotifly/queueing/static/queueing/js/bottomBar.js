// handy util for updating the active icon
function updateActiveIcon(icon) {
  document.querySelectorAll(".bottom-bar .nav-icon").forEach(function (icon) {
    icon.classList.remove("active");
  });
  icon.classList.add("active");
}

// DJ Page
function loadDJPage() {
  updateActiveIcon(document.getElementById("dj-icon"));

  if (followingDJ) {
    mainContent.innerHTML = `
            <div class="row">
                <div class="col-12">
                    <h1>DJ</h1>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <p>
                        You are following ${followingDJ}
                    </p>
                </div>
            </div>`;
  } else {
    mainContent.innerHTML = `
    <div class="row">
        <div class="col-12">
            <h1>Follow a DJ to Queue Songs.</h1>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
          <form id="follow-dj-form" onSubmit="return followDJ();">
              <div class="form-group">
                  <label for="follow-dj">DJ Name</label>
                  <input type="text" class="form-control big-ole-form-input" id="follow-dj" required>
              </div>
              <button id="follow-dj-btn" class="btn btn-primary btn-lg form-submit big-ole-btn">
                  Submit
              </button>
          </form>
        </div>
    </div>`;
  }
}

// Profile Page
function loadProfilePage() {
  updateActiveIcon(document.getElementById("profile-icon"));
  if (IAmDJ) {
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
                        You are DJ ${IAmDJ}
                    </p>
                    <button class="btn btn-primary big-ole-btn" onclick="shuffle()">Shuffle</button>
                </div>
            </div>
            <div class="row">
                <div class="col-12">
                    <p id="shuffle-message" style="padding-top: 10%; display: none;">
                        Shuffle Message
                    </p>
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
                        <button id="connect-with-spotify" class="btn btn-primary btn-lg">
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

// Queue Page
function loadQueuePage() {
  updateActiveIcon(document.getElementById("queue-icon"));
  mainContent.innerHTML = "";
  mainContent.innerHTML = `
    <div class="row">
        <div class="col-12">
            <p>
                Queue Songs
            </p>
        </div>
    </div>
    <div class="row">
        <div class="col-12">
            <div id="queue-container" class="queue-container">
                <input type="text" class="form-control big-ole-form-input" id="queue-song-input" placeholder="Search for a song">
            </div>
            <button class="btn btn-primary big-ole-btn" onclick="queue()">queue</button>
        </div>
    </div>
    `;
}

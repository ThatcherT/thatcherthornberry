
// Queue Page
function loadQueuePage() {
    updateActiveIcon(document.getElementById("queue-icon"));
    mainContent.innerHTML = "";
    mainContent.innerHTML = `
      <p id="queue-message"></p>
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
              <button class="btn btn-primary big-ole-btn" onclick="search()">Search</button>
          </div>
      </div>
      <div id="search-results" class="search-box">
      </div>
      `;
}


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
  
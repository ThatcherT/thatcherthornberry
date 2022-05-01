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
  
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
        }
    })
}

// DJ Page
async function loadDJPage() {
    updateActiveIcon(document.getElementById("dj-icon"));

    if (getFollowingDJ()) {
        mainContent.innerHTML = `
              <div class="row">
                  <div class="col-12">
                      <h1>DJ</h1>
                  </div>
              </div>
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
              </div>`;
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
                        ${djObj.djs.map(dj => `<option value="${dj}">${dj}</option>`).join("")}
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
        $('#dj-select').selectpicker().selectpicker('refresh');
    }
}

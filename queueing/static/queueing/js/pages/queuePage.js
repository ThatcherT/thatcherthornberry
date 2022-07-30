
// Queue Page
function loadQueuePage() {
    updateActiveIcon(document.getElementById("queue-icon"));
    // see if user is following a dj
    if (getFollowingDJ()) {
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
                <button class="btn btn-primary big-ole-btn" onclick="search()">Search</button>`
        mainContent.innerHTML += getIAmDJ() ? `<button class="btn btn-primary big-ole-btn" onclick="suggest()">Suggest</button>`: '';
        mainContent.innerHTML += `</div>
        </div>
        <div id="search-results" class="search-box">
        </div>
        `;
    } else {
        mainContent.innerHTML = "You aren't following a DJ. Can't queue!";
    }
}


// from an array of objects, add rows to the div with id="search-results"
// each object should have its on row
// it should have columns that show relevant information like:
//  songObj.name
//  songObj.album.images[0] (highest res)
//  songObj.artists which is an array of objects that have attribute name
function showSongsOnQueuePage(songObjs) {
    const searchResults = document.getElementById("search-results");
    // empty any previous results
    searchResults.innerHTML = "";
    // add rows to div
    // only use the first 5 results
    songObjs.slice(0, 5).forEach(function (songObj) {
      const row = getSongRowHTML(songObj);
      // append this row to the div
      searchResults.appendChild(row);
  
      // add a click event to the row
      row.addEventListener("click", async function () {
        // get clicked element
        let clickedElement = event.target;
        // get the data-uri attribute from the clicked element
        let URI = clickedElement.getAttribute("data-uri");
        // while no URI
        let safeCounter = 0;
        while (!URI) {
          // get the parent of the clicked element
          clickedElement = clickedElement.parentElement;
          // get the data-uri attribute from the parent element
          URI = clickedElement.getAttribute("data-uri");
          safeCounter++;
          // if we have gone too far, break
          if (safeCounter > 5) {
            console.log("could not find URI!!!!! badness");
            break;
          }
        }
        // if we have a URI, we got the row containing the song data
        if (URI) {
          // add the song to the queue
          const response = await queue(URI);
          if (response.success) {
            // change the color of clicked element to green
            clickedElement.style.color = "green";
            // get element with id "queue-message"
            const queueMessage = document.getElementById("queue-message");
            // change the text of the element to "added to queue"
            queueMessage.innerHTML = "Queued!";
            // add class success-message
            queueMessage.classList.remove("error-message");
            queueMessage.classList.add("success-message");
          } else {
            // change the color of clicked element to red
            clickedElement.style.color = "red";
            // get element with id "queue-message"
            const queueMessage = document.getElementById("queue-message");
            // see if response.error contains "NO_ACTIVE_DEVICE"
            if (response.error.includes("NO_ACTIVE_DEVICE")) {
              queueMessage.innerHTML = "Your DJ isn't playing music!";
            } else {
              queueMessage.innerHTML = response.error;
            }
            // add class error-message
            queueMessage.classList.remove("success-message");
            queueMessage.classList.add("error-message");
          }
        } else {
          console.log("since there is no URI... idk what you want me to do here :/");
        }
      });
    });
  }
  
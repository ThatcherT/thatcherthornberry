/*
This document contains some helpful utils for shuffling, following, and queueing, loadpage, other.
*/

function getFollowingDJ() {
  return jQuery.data(document.body, "followingDJ")
}

function getIAmDJ() {
  return jQuery.data(document.body, "IAmDJ")
}

// STARTUP SCRIPT RUNS EVERY TIME!!!!!
loadPage();

function loadPage() {
  // check if any DJ relations exist
  if (getFollowingDJ() || getIAmDJ()) {
    const bottomBar = document.getElementById("bottom-bar");
    bottomBar.style.display = "";
    if (getIAmDJ()) {
      loadProfilePage();
    } else {
      loadDJPage();
    }
  } else {
    loadWelcomePage();
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

    // IMPORTANT: this is the songs unique identifier
    const URI = songObj.uri;
    // create row, this is all the song data
    const row = document.createElement("div");
    row.classList.add("row", "search-item");
    // add an attribute data-uri to the row
    row.setAttribute("data-uri", URI);

    // album image
    const albumImageCol = document.createElement("div");
    albumImageCol.classList.add("col-3");
    row.appendChild(albumImageCol);
    const albumImage = document.createElement("img");
    albumImage.src = songObj.album.images[1].url;
    albumImage.style.width = "128px";
    albumImage.style.height = "128px";
    albumImageCol.appendChild(albumImage);

    // I feel like I should clarify what I am trying to achieve here...
    // the second column should be a div with a class of "col-10"
    // this column will contain two rows:
    // the first row will have the song name
    // the second row will have the artist names
    // technically, each row will have a single column as bootstrap requires (I think?)

    // this is the main column, containing the song details
    const songDetails = document.createElement("div");
    songDetails.classList.add("col");
    // append this column to the row
    row.appendChild(songDetails);

    // the first row will have the song name
    const songNameRow = document.createElement("div");
    songNameRow.classList.add("row", "song-title");
    // append this row to the main column
    songDetails.appendChild(songNameRow);
    // technically, the name will be in a column, in the row
    const songName = document.createElement("div");
    songName.classList.add("col", "text-left");
    // limit name to 30 characters, if greater than 30 characters, add ...
    if (songObj.name.length > 30) {
      songName.innerHTML = songObj.name.substring(0, 27) + "...";
    } else {
      songName.innerHTML = songObj.name;
    }
    // append this column to the row
    songNameRow.appendChild(songName);

    // the second row will have the artist names
    const songArtistRow = document.createElement("div");
    songArtistRow.classList.add("row", "song-artist");
    // append this row to the main column
    songDetails.appendChild(songArtistRow);
    // technically, the artist names will be in a column, in the row
    const songArtist = document.createElement("div");
    songArtist.classList.add("col", "text-left");
    const artistStr = songObj.artists.map(function (artist) {
      return artist.name;
    }).join(", ");
    // limit artist names to 30 characters, if greater than 30 characters, add ...
    if (artistStr.length > 40) {
      songArtist.innerHTML = artistStr.substring(0, 37) + "...";
    } else {
      songArtist.innerHTML = artistStr;
    }
    // append this column to the row
    songArtistRow.appendChild(songArtist);

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

// handy util for updating the active icon
function updateActiveIcon(icon) {
  document.querySelectorAll(".bottom-bar .nav-icon").forEach(function (icon) {
    icon.classList.remove("active");
  });
  icon.classList.add("active");
}

function copyInviteToClipboard(setting) {
  // the invite link is qsongs.thatcherthornberry.com/invite-link/<IAmDJ>
  let inviteLink;
  if (setting === 'Follow') {
    const followDj = getFollowingDJ()
    inviteLink = 'https://qsongs.thatcherthornberry.com/invite-link/' + followDj;
  } else {

    const IAmDJ = getIAmDJ();
    inviteLink = `https://qsongs.thatcherthornberry.com/invite-link/${IAmDJ}/`;
  }
  // copy to clipboard
  navigator.clipboard.writeText(inviteLink);
  // show message
  const profilePageMessage = document.getElementById("profile-page-message");
  profilePageMessage.classList.remove("error-message");
  profilePageMessage.classList.add("success-message");
  profilePageMessage.innerHTML = "Copied to clipboard!";
}
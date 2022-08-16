

// send an ajax request with local storage data and data from an input element
// this request should return a list of songs searched on spotify
function search() {
    const song = document.getElementById("queue-song-input").value;
    $.ajax({
        url: "/ajax/search/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            song: song,
        },
        dataType: "json",
        success: function (data) {
            songObjs = data.song_lst;
            showSongsOnQueuePage(songObjs);
        }
    });
}

function suggest() {
    $.ajax({
        url: "/ajax/suggest/",
        type: "GET",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            iam: getIAmDJ(),
        },
        success: function (data) {
            songObjs = data.song_lst
            showSongsOnQueuePage(songObjs);
        }
    });
        
}


function getNowPlaying() {
    return $.ajax({
        url: "/ajax/now-playing/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            dj: getFollowingDJ(),
        },
        success: function (data) {
            return data.songObj;
        }
    });
}


// send an ajax request with local storage data and data from an input element
// this request should return a msg indicating queue success or failure
function queue(URI) {
    return $.ajax({
        url: "/ajax/queue/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            uri: URI,
            dj: getFollowingDJ(),
        },
        success: function (data) {
            return data.msg;
        }
    });
}



// send ajax to server and shuffle for IAmDJ
function shuffle() {
    $.ajax({
        url: "/ajax/shuffle/",
        data: {
            IAmDJ: getIAmDJ(),
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        type: "POST",
        dataType: "json",
        success: function (data) {
            // shuffle success message
            document.getElementById("profile-page-message").style.display = "";
            document.getElementById("profile-page-message").style.color = "green";
            document.getElementById("profile-page-message").innerHTML = "Shuffled!";
        },
        error: function (xhr, status, error) {
            // shuffle error message
            document.getElementById("profile-page-message").style.display = "";
            document.getElementById("profile-page-message").style.color = "red";
            document.getElementById("profile-page-message").innerHTML = "Some error.. sorry";
        },
    });
}

function followDJ() {
    // store dj in session
    const followingDJ = document.getElementById("dj-select").value;
    // if value is 'Select a DJ', show error message
    if (followingDJ === "Select a DJ") {
        document.getElementById("follow-dj-error").innerHTML = "Use the dropdown!";
        return;
    }
    $.ajax({
        url: "/ajax/follow-dj/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            followingDJ: followingDJ,
        },
        dataType: "json",
        success: function (data) {
            // update jQuery data
            jQuery.data(document.body, "followingDJ", followingDJ);
            // weird bug that causes invisible bottom bar..
            const bottomBar = document.getElementById("bottom-bar");
            bottomBar.style.display = "";
            // show the DJ Page
            loadDJPage();
            return true;
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
            console.log(status, error);
            document.getElementById("follow-dj-error").innerHTML = "IDK what happened";
            return false;
        },
    });
}


// remove the followDJ from django session
function unfollowDJ() {
    $.ajax({
        url: "/ajax/unfollow-dj/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            followingDJ: getFollowingDJ(),
        },
        dataType: "json",
        success: function (data) {
            // update jQuery data
            jQuery.data(document.body, "followingDJ", null);
            loadDJPage();
            return true;
        },
        error: function (xhr, status, error) {
            alert(xhr.responseText);
            console.log(status, error);
            document.getElementById("follow-dj-error").innerHTML = "IDK what happened";
            return false;
        },
    });
}
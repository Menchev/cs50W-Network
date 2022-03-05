document.addEventListener('DOMContentLoaded', function() {

    // get the root div view
    const view = document.querySelector('#followInfo');

    // get the user id
    const userID = document.querySelector('#userID').value

    // create the followBtn
    const followBtn = document.createElement('button')

    // create a div for the followers and following count
    const followCount = document.createElement('div');
    followCount.className = "p-3"

    // fetch a query for the followinfo
    fetch('/profile/' + userID, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(response => {

        // check count of the follow info
        followCount.innerHTML = `
            <span>Followers: ${response.followers}<span>
            <span>Following: ${response.following}</span>
            `
        // append the counts to the root div
        view.appendChild(followCount)
        
        // render the button only if the profile is visited not by the owner
        if (!response.is_users_profile){

            //check if the user is a follower already
            followBtn.className = response.is_follower ? "btn btn-light ms-3" : "btn btn-primary ms-3"
            followBtn.innerHTML = response.is_follower ? "Unfollow" : "Follow"

            // append the button to the view
            view.appendChild(followBtn);
        }

        // when the follow/unfollow btn is clicked
        followBtn.addEventListener('click', () => {
            fetch('/profile/' + userID, {
                method: 'PUT'
            })
            .then(response => response.json())
            .then(response => {

                // switch button depending on follow status
                followBtn.className = response.is_follower ? "btn btn-light ms-3" : "btn btn-primary ms-3"
                followBtn.innerHTML = response.is_follower ? "Unfollow" : "Follow"

                // update count of the follow info
                followCount.innerHTML = `
                <span>Followers: ${response.followers}<span>
                <span>Following: ${response.following}</span>
                `
            })
        })

    })

})
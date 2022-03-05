document.addEventListener('DOMContentLoaded', () => {

    // get all buttons id's
    const editBtns = document.querySelectorAll('#editBtn')

    // loop through and add an event listener to each one
    editBtns.forEach(editBtn => {
        editBtn.onclick = () => {

            // hide the post
            const post = editBtn.parentElement;
            post.style.display = 'none';

            // get the root div view for the edit display
            const editView = document.querySelector('#editPost')

            // create and display the edit view
            const div = document.createElement('div')
            div.className = "container border mb-4 mt-4 p-4 rounded"
            div.innerHTML = `
                <textarea id="editContent"></textarea>
                
                `
            // create and append a button for submitting
            const button = document.createElement('button')
            button.className = "btn btn-primary"
            button.innerHTML = "Save"

            div.appendChild(button)

            editView.appendChild(div)

            // if the save button is clicked
            button.addEventListener('click', () => {
                console.log(post.dataset.post_id)
                console.log(document.querySelector('#editContent').value)
                const content = document.querySelector('#editContent').value
                fetch('edit_post', {
                    method: 'POST',
                    body: JSON.stringify({
                        post_id: post.dataset.post_id,
                        content: content
                    })
                })
                .then(
                    post.querySelector('#post-content').innerHTML = content,
                    post.style.display = 'block',
                    div.style.display = 'none'
                )
            })
        } 
    })

})


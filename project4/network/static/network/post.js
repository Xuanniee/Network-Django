// Wait for the entire DOM to be loaded
document.addEventListener('DOMContentLoaded', function () {

    // Adding Event Listeners to ALL the Edit Button
    const edit_button_list = document.querySelectorAll('.Edit-Button');
    edit_button_list.forEach(button => {
        // Gets Post ID from Button
        const post_id = button.value;
        button.addEventListener('click', button => {
            // Prevent Form Submission
            button.preventDefault();
            edit_post(post_id);
        })
    })

    // Adding Event Handlers to All Cancel Buttons
    const cancel_button_list = document.querySelectorAll('.Cancel-Edit-Button');
    cancel_button_list.forEach(cancel_button => {
        // Post ID
        const post_id = cancel_button.value;
        cancel_button.addEventListener('click', cancel_button => {
            cancel_button.preventDefault();
            stop_edit_post(post_id);
        })
    })

    // Add Event Listeners to ALL Save Button to Commit Changes
    const edit_save_button_list = document.querySelectorAll(`.Save-Edit-Button`);
    edit_save_button_list.forEach(save_button => {
        const post_id = save_button.value;
        save_button.addEventListener('click', save_button => {
            save_button.preventDefault();
            save_post(post_id);
        })
    })

    // Adding Event Listener for PUT Request to update Post
    const like_button_list = document.querySelectorAll('.Post-Like-Button');
    const unlike_button_list = document.querySelectorAll('.Post-Unlike-Button');

    like_button_list.forEach(like_button => {
        const post_id = like_button.value;
        like_button.addEventListener('click', () => {
            like_post(post_id, true);
        })
    })
    
    unlike_button_list.forEach(unlike_button => {
        const post_id = unlike_button.value;
        unlike_button.addEventListener('click', () => {
            like_post(post_id, false);
        })
    })

    // Default
    // Hide ALL the Edit View
    const edit_view_list = document.querySelectorAll('.Edit-View');
    edit_view_list.forEach(element => {
        element.style.display = 'none';
    })

    // Show ALL the Posts
    const post_view_list = document.querySelectorAll('.Post-View');
    post_view_list.forEach(element => {
        element.style.display = 'block';
    })

    // Hide Unlike and Show Like
    like_button_list.forEach(element => {
        element.style.display = 'block';
    })
    unlike_button_list.forEach(element => {
        element.style.display = 'none';
    })

})

// Edit Post
function edit_post(post_id) {    
    // Select the Post and Edit Views
    const edit_form_to_show = document.querySelector(`#Edit-Form-${post_id}`);
    const post_to_hide = document.querySelector(`#Post-${post_id}`);

    // Select Buttons to Hide
    const buttons_to_hide = document.querySelector(`#Post-Buttons-${post_id}`);
    const edit_button_to_hide = document.querySelector(`#Edit-Button-${post_id}`);

    // Hide Post-View and Show Edit-View and Post-Buttons
    post_to_hide.style.display = 'none';
    buttons_to_hide.style.display = 'none';
    edit_button_to_hide.style.display = 'none';
    edit_form_to_show.style.display = 'block';

    // Retrieve the Original Post
    const original_post_content = document.querySelector(`#Post-Contents-${post_id}`).innerHTML;

    // Place OP in Textarea
    edit_textarea = document.querySelector(`#Edit-Body-${post_id}`);
    edit_textarea.value = original_post_content.trim();                 // Removes Trailing and Start Whitespace

    return false;
}

function save_post(post_id) {
    // Retrieve Edited Content
    const edited_post_content = document.querySelector(`#Edit-Body-${post_id}`).value;

    // Retrieve CSRF Token Value to prevent Error 403 when saving edits
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Convert Timestamp from API to more readable formats
    let edited_timestamp = new Date();
    edited_timestamp = edited_timestamp.toLocaleString();

    // PUT Request to Update Posts
    fetch(`/posts/${post_id}`, {
        method: 'get'
    })
    .then(response => response.json())
    .then(first_response => {

        // Determine if this is first edit!!
        const first_edit = first_response["post_edited"];

        fetch(`/posts/${post_id}`, {
            method: "put",
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json; charset=UTF-8'
            },
            body: JSON.stringify({
                post_content: edited_post_content,
                post_edited: true,
                post_edited_timestamp: edited_timestamp,
            })
        })
        .then(response => response.json())
        .then(result => {

            // First Edit
            if (first_edit === false) {
                // GET Request to retrieve Edited Post
                const post_div = document.querySelector(`#Post-Contents-${post_id}`);
                const post_timestamp = document.querySelector(`#Post-Timestamp-${post_id}`);
                fetch(`/posts/${post_id}`, {
                    method: "get"
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result["post_content"]);
                    // "Refresh" Post Contents
                    post_div.innerHTML = result["post_content"];
                    // "Refresh" Post Timestamp
                    post_timestamp.innerHTML = `Edited on: ${result["post_edited_timestamp"]}`;
                })
            }

            // Subsequent Edits
            else {
                // GET Request to retrieve Edited Post
                const post_div = document.querySelector(`#Post-Contents-${post_id}`);
                const post_timestamp = document.querySelector(`#Post-Edited-Timestamp-${post_id}`);
                fetch(`/posts/${post_id}`, {
                    method: "get"
                })
                .then(response => response.json())
                .then(result => {
                    // "Refresh" Post Contents
                    post_div.innerHTML = result["post_content"];
                    // Make Timestamp readable
                    const readable_timestamp = result["post_edited_timestamp"];
                    readable_timestamp = readable_timestamp.toLocaleDateString();
                    // "Refresh" Post Timestamp
                    post_timestamp.innerHTML = `Edited on: ${readable_timestamp}`;
                })
            }
        })
    })

    // Hide the Edit and Show Edited Post
    document.querySelector(`#Post-${post_id}`).style.display = 'block';
    document.querySelector(`#Post-Buttons-${post_id}`).style.display = 'block';
    document.querySelector(`#Edit-Button-${post_id}`).style.display = 'block';
    
    document.querySelector(`#Edit-Form-${post_id}`).style.display = 'none';

}

// Stop Editing Post. Discard Changes
function stop_edit_post(post_id) {
    // Select the Post and Edit Views
    const edit_form_to_show = document.querySelector(`#Edit-Form-${post_id}`);
    const post_to_hide = document.querySelector(`#Post-${post_id}`);

    // Select Buttons to Hide
    const buttons_to_hide = document.querySelector(`#Post-Buttons-${post_id}`);
    const edit_button_to_hide = document.querySelector(`#Edit-Button-${post_id}`);

    // Hide Post-View and Show Edit-View and Post-Buttons
    post_to_hide.style.display = 'block';
    buttons_to_hide.style.display = 'block';
    edit_button_to_hide.style.display = 'block';
    edit_form_to_show.style.display = 'none';
}

function like_post(post_id, like) {
    // Retrieve CSRF Token Value to prevent Error 403 when saving edits
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Retrieve Current Number of Likes
    const num_of_likes_span = document.querySelector(`#Num-Likes-${post_id}`);
    var num_of_likes = num_of_likes_span.innerHTML;

    if (like === true) {
        // Increment Likes
        num_of_likes = parseInt(num_of_likes) + 1;
    }
    else if (like === false) {
        // Decrement Likes
        num_of_likes = parseInt(num_of_likes) - 1;
    }

    // PUT Request to add Current User into Post's Likes List [UPDATE]
    fetch(`/posts/${post_id}`, {
        method: "put",
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        body: JSON.stringify({
            post_num_likes: num_of_likes             
        })
    })
    .then(response => response.json())
    .then(json_response => {
        console.log(json_response)
        // "Refresh" Post Number of Likes
        num_of_likes_span.innerHTML = json_response["post_num_likes"];
    })

    // Hiding of Buttons
    const like_button = document.querySelector(`#Post-Like-Button-${post_id}`);
    const unlike_button = document.querySelector(`#Post-Unlike-Button-${post_id}`);

    if (like === true) {
        // Hide Like Button and Show Unlike Button
        like_button.style.display = 'none';
        unlike_button.style.display = 'block';
    }
    else if (like === false) {
        // Hide Unlike Button and Show Like Button
        like_button.style.display = 'block';
        unlike_button.style.display = 'none';
    }
}

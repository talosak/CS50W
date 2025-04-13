document.addEventListener('DOMContentLoaded', () => {

    // Get profile_id
    var profile_id = document.querySelector('#user_id').value

    renderUserPosts(profile_id);


});

function renderUserPosts(profile_id) {
    // Get posts
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        // Paginate posts
        fetch('/paginate', {
            method: "POST",
            body: JSON.stringify({
                "postList": posts,
                "page_id": page_id,
            })
        })
        .then(response => response.json())
        .then(paginatedPosts => {
        // Render posts
            paginatedPosts.list.forEach(post => {
                if (parseInt(post.creator.id) === parseInt(profile_id)) {
                    let div = document.createElement('div');
                    div.classList.add("p-3", "my-2", "border", "border-secondary");
                    let usernameElement = document.createElement('h3');
                    usernameElement.innerHTML = `<strong>${post.creator.username}</strong>`;
                    div.append(usernameElement);
                    let contentElement = document.createElement('h4');
                    contentElement.innerHTML = `${post.content}`;
                    div.append(contentElement);
                    let timestampElement =  document.createElement('h4');
                    timestampElement.innerHTML = `${post.timestamp}`;
                    div.append(timestampElement);
                    let likesElement = document.createElement('div');
                    likesElement.classList.add("p-1", "border", "border-secondary");
                    likesElement.style = "font-size:120%;width:fit-content;";
                    likesElement.innerHTML = `Likes: ${post.likers.length}`;
                    div.append(likesElement);

                    document.querySelector('#posts-container').append(div);
                }
            });
        }); 
    });
}
document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#create-post-form').addEventListener('submit', createPost);

    document.querySelector('#create-post-submit').disabled = true;
    document.querySelector('#create-post-content').onkeyup = () => {
        if (document.querySelector('#create-post-content').value.length > 0) {
            document.querySelector('#create-post-submit').disabled = false;
        } else {
            document.querySelector('#create-post-submit').disabled = true;
        }
    }
    document.querySelector('#create-post-form').onsubmit = function() {
        document.querySelector('#create-post-content').value = '';
        document.querySelector('#create-post-submit').disabled = true;
    }

    renderPosts();

});

function createPost(event) {
    event.preventDefault();
    fetch('/posts', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        credentials: 'same-origin',
        body: JSON.stringify({
            content: document.querySelector('#create-post-content').value
        })
    })
    .then(response => response.json())

    document.querySelector('#create-post-content').value = '';
}

function renderPosts() {
    // Get posts
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        // Render posts
        posts.forEach(post => {
            let div = document.createElement('div');
            div.classList.add("p-3", "my-2", "border", "border-secondary");
            let usernameElement = document.createElement('h3');
            usernameElement.innerHTML = `<strong>${post.creator.username}</strong>`;
            usernameElement.style.cursor = 'pointer';
            usernameElement.addEventListener('click', () => {
                baseUrl = document.querySelector("#data").dataset.baseUrl;
                window.location.href = baseUrl.replace("0", post.creator.id);
            });
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
        }); 
    });
}

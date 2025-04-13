document.addEventListener('DOMContentLoaded', () => {
    
    var page_id = document.querySelector('#page_id').value
    var currentUser_id = document.querySelector('#current-user-id').value
    var is_authenticated = document.querySelector('#current-user-authentication').value
    
    document.querySelector('#create-post-form').addEventListener('submit', createPost);

    document.querySelector('#create-post-submit').disabled = true;
    document.querySelector('#create-post-content').onkeyup = () => {
        if (document.querySelector('#create-post-content').value.length > 0 && is_authenticated === "True") {
            document.querySelector('#create-post-submit').disabled = false;
        } else {
            document.querySelector('#create-post-submit').disabled = true;
        }
    }
    document.querySelector('#create-post-form').onsubmit = function() {
        document.querySelector('#create-post-content').value = '';
        document.querySelector('#create-post-submit').disabled = true;
    }

    renderPosts(page_id, currentUser_id, is_authenticated);

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

function renderPosts(page_id, currentUser_id, is_authenticated) {
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
        .then(page => {
            // Render posts
            page.list.forEach(post => {
                let div = document.createElement('div');
                div.classList.add("p-3", "my-2", "border", "border-secondary");
                let usernameElement = document.createElement('h3');
                usernameElement.innerHTML = `<strong>${post.creator.username}</strong>`;
                usernameElement.style.cursor = 'pointer';
                usernameElement.addEventListener('click', () => {
                    baseUrl = document.querySelector("#data").dataset.baseUrl;
                    window.location.href = baseUrl.replace("0", post.creator.id);
                });
                let editElement = document.createElement('h4');
                editElement.innerHTML = `<span style="color:dodgerblue;">Edit</span>`;
                editElement.style.cursor = 'pointer';
                let editAreaElement = document.createElement('div');
                let editPostForm = document.createElement('form');
                let editPostTextarea = document.createElement('textarea');
                editPostTextarea.style = "width:100%; height:150px";
                editPostTextarea.classList.add("form-control");
                editPostTextarea.value = post.content;
                let editPostSubmit = document.createElement('input');
                editPostSubmit.type = 'submit';
                editPostSubmit.classList.add("btn", "btn-primary", "mt-2");
                editPostSubmit.value = "Save";
                editPostForm.append(editPostTextarea);
                editPostForm.append(editPostSubmit);
                editAreaElement.append(editPostForm);
                editAreaElement.style.display = 'none';
                let contentElement = document.createElement('h4');
                contentElement.innerHTML = `${post.content}`;
                let timestampElement = document.createElement('h4');
                timestampElement.innerHTML = `${post.timestamp}`;
                let likesElement = document.createElement('div');
                likesElement.classList.add("p-1", "border", "border-secondary");
                likesElement.style = "font-size:120%;width:fit-content;";
                likesElement.innerHTML = `Likes: ${post.likers.length}`;
                if (post.likers.includes(parseInt(currentUser_id))) {
                    likesElement.style.fontWeight = 'bold';
                    likesElement.style.backgroundColor = 'lightgray';
                } else {
                    likesElement.style.fontWeight = 'normal';
                    likesElement.style.backgroundColor = 'white';
                }
                if (is_authenticated === "True") {
                    likesElement.style.cursor = 'pointer';
                    likesElement.addEventListener('click', () => {
                        if (post.likers.includes(parseInt(currentUser_id))) {
                            likesElement.style.fontWeight = 'normal';
                            likesElement.style.backgroundColor = 'white';
                            likesElement.innerHTML = `Likes: ${post.likers.length - 1}`;
                            unlike(post.id, currentUser_id);
                        } else {
                            likesElement.style.fontWeight = 'bold';
                            likesElement.style.backgroundColor = 'lightgray';
                            likesElement.innerHTML = `Likes: ${post.likers.length + 1}`;
                            like(post.id, currentUser_id);
                        }
                    });
                }
                editElement.addEventListener('click', () => {
                    editAreaElement.style.display = 'block';
                    editElement.innerHTML = '';
                    contentElement.innerHTML = '';
                    editPostForm.addEventListener('submit', event => {
                        event.preventDefault();
                        fetch('/posts', {
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            method: 'PUT',
                            credentials: 'same-origin',
                            body: JSON.stringify({
                                content: editPostTextarea.value,
                                id: post.id,
                            })
                        })
                        .then(response => response.json());
                        contentElement.innerHTML = editPostTextarea.value;
                        editElement.innerHTML = `<span style="color:dodgerblue;">Edit</span>`;
                        editAreaElement.style.display = 'none';
                    });
                });
                if (parseInt(currentUser_id) === parseInt(post.creator.id)) {
                    editElement.style.display = 'block';
                } else {
                    editElement.style.display = 'none';
                }
                div.append(usernameElement);
                div.append(editElement);
                div.append(editAreaElement);
                div.append(contentElement);
                div.append(timestampElement);
                div.append(likesElement);
                document.querySelector('#posts-container').append(div);  
            });
            if (!page.hasPrevious) {
                document.querySelector('#previous-page').style.display = 'none';
            }
            if (!page.hasNext) {
                document.querySelector('#next-page').style.display = 'none';
            }
            if (page.pageCount === 1) {
                document.querySelector('#second-page').style.display = 'none';
                document.querySelector('#third-page').style.display = 'none';
            }
            if (page.pageCount === 2) {
                document.querySelector('#third-page').style.display = 'none';
            }
        });     
    });
}

function like(post_id, currentUser_id) {
    fetch('/like', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'PUT',
        credentials: 'same-origin',
        body: JSON.stringify({
            post_id: post_id,
            user_id: currentUser_id,
        })
    })
    .then(response => response.json());
}

function unlike(post_id, currentUser_id) {
    fetch('/unlike', {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'PUT',
        credentials: 'same-origin',
        body: JSON.stringify({
            post_id: post_id,
            user_id: currentUser_id,
        })
    })
    .then(response => response.json());
}
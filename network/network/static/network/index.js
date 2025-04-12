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
            console.log(post)
            let div = document.createElement('div');
            div.innerHTML = `<div class="p-3 my-2 border border-secondary">
                <h3><strong>${post.creator}</strong></h3>
                <h4>${post.content}</h4>
                <h4>${post.timestamp}</h4>
                <div id="likes" class="p-1 border border-secondary" style="font-size:120%;width:fit-content;">Likes: ${post.likers.length}</div>
            </div>`;
            document.querySelector('#posts-container').append(div);
        }); 
    });
}

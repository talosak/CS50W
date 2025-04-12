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

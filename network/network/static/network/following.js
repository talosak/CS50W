document.addEventListener('DOMContentLoaded', () => {

    var page_id = document.querySelector('#page_id').value

    // Get followList
    var followIDList = []
    fetch('/following', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(followList => {
        // Create list of id's
        followList.forEach(user => {
            followIDList.push(user.id);
        });
        renderFollowingPosts(followIDList, page_id);
    });
});

function renderFollowingPosts(followIDList, page_id) {
    // Get posts
    fetch('/posts')
    .then(response => response.json())
    .then(posts => {
        // Paginate posts
        let postArray = [];
        posts.forEach(postForArray => {
            if (followIDList.includes(postForArray.creator.id)) {
                postArray.push(postForArray);
            }
        })
        fetch('/paginate', {
            method: "POST",
            body: JSON.stringify({
                "postList": postArray,
                "page_id": page_id,
            })
        })
        .then(response => response.json())
        .then(page => {
            // Render posts
            page.list.forEach(post => {
                if (followIDList.includes(post.creator.id)) {
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
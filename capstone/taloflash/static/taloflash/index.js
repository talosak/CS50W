function likeSet(set_id) {
    let likeButton = document.querySelector(`#likeSetButton-${set_id}`);
    if (likeButton.innerHTML === "Like") {
        likeButton.innerHTML = "Unlike";
        likeButton.classList.remove("btn-primary");
        likeButton.classList.add("btn-secondary");
    } else {
        likeButton.innerHTML = "Like";
        likeButton.classList.remove("btn-secondary");
        likeButton.classList.add("btn-primary");
    }
}

function saveSet(set_id) {
    let saveButton = document.querySelector(`#saveSetButton-${set_id}`);
    if (saveButton.innerHTML === "Save") {
        saveButton.innerHTML = "Unsave";
        saveButton.classList.remove("btn-primary");
        saveButton.classList.add("btn-secondary");
    } else {
        saveButton.innerHTML = "Save";
        saveButton.classList.remove("btn-secondary");
        saveButton.classList.add("btn-primary");
    }
}
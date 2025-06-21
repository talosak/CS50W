function deleteFlashcard(flashcard_id, set_id) {
    fetch(`/sets/${set_id}/${flashcard_id}`, {
        method: "DELETE",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'same-origin',
    });

    flashcard = document.querySelector(`#flashcard-${flashcard_id}`);
    flashcard.innerHTML = '';
    flashcard.classList = '';
}
function deleteFlashcard(flashcard_id, set_id) {
    fetch(`/sets/${set_id}/alterFlashcard/${flashcard_id}`, {
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

function displayEditFlashcard(flashcard_id, set_id) {
    baseFlashcard = document.querySelector(`#flashcard-base-${flashcard_id}`);
    editFlashcardForm = document.querySelector(`#flashcard-edit-form-${flashcard_id}`);
    baseFlashcard.classList.add("d-none");
    baseFlashcard.classList.remove("d-block");
    editFlashcardForm.classList.add("d-block");
    editFlashcardForm.classList.remove("d-none");
}

function saveFlashcardEdit(flashcard_id, set_id) {
    baseFlashcard = document.querySelector(`#flashcard-base-${flashcard_id}`);
    editFlashcardForm = document.querySelector(`#flashcard-edit-form-${flashcard_id}`);
    editFlashcardForm.classList.add("d-none");
    editFlashcardForm.classList.remove("d-block");
    baseFlashcard.classList.add("d-block");
    baseFlashcard.classList.remove("d-none");

    flashcardFront = document.querySelector(`#flashcard-front-${flashcard_id}`);
    flashcardBack = document.querySelector(`#flashcard-back-${flashcard_id}`);
    flashcardImage = document.querySelector(`#flashcard-image-${flashcard_id}`);
    newFlashcardFront = document.querySelector(`#flashcard-edit-front-${flashcard_id}`);
    newFlashcardBack = document.querySelector(`#flashcard-edit-back-${flashcard_id}`);
    newFlashcardImageURL = document.querySelector(`#flashcard-edit-imageURL-${flashcard_id}`);

    flashcardFront.innerHTML = newFlashcardFront.value;
    flashcardBack.innerHTML = newFlashcardBack.value;
    flashcardImage.src = newFlashcardImageURL.value;

    fetch(`/sets/${set_id}/alterFlashcard/${flashcard_id}`, {
        method: "PUT",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'same-origin',
        body: JSON.stringify({
            newFront: newFlashcardFront.value,
            newBack: newFlashcardBack.value,
            newImageURL: newFlashcardImageURL.value,
        }),
    });
}
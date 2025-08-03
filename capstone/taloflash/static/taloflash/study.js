// This has to be a global variable
var flashcardIndex = 0;

document.addEventListener('DOMContentLoaded', () => {
    let pathnameArray = window.location.pathname.split("/");
    var flashset_id = pathnameArray[2];

    fetch(`/sets/${flashset_id}/study`, {
        method: "POST",
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(flashcards => {
        console.log(flashcards);
        document.querySelector("#learnedButton").addEventListener('click', () => learned(flashcards));
        document.querySelector("#notLearnedButton").addEventListener('click', () => notLearned(flashcards));
        displayFlashcard(flashcards);
    });
});

function flip() {
    let flashcardFront = document.querySelector("#flashcardFront");
    let flashcardBack = document.querySelector("#flashcardBack");

    if (flashcardFront.classList.contains("d-none")) {
        flashcardBack.classList.add("d-none");
        flashcardFront.classList.remove("d-none");
    } else {
        flashcardFront.classList.add("d-none");
        flashcardBack.classList.remove("d-none");
    }

}

function displayFlashcard(flashcards) {
    let flashcard = flashcards[flashcardIndex];
    let frontText = document.querySelector('#studyFlashcardFrontText');
    let backText = document.querySelector('#studyFlashcardBackText');
    let frontImageURL = document.querySelector('#studyFlashcardFrontImageURL');
    let backImageURL = document.querySelector('#studyFlashcardBackImageURL');

    frontText.innerHTML = flashcard.front;
    backText.innerHTML = flashcard.back;
    frontImageURL.src = flashcard.imageURL;
    backImageURL.src = flashcard.imageURL;
}

function learned(flashcards) {
    // If current flashcard is the last one, do something
    if (flashcardIndex === flashcards.length - 1) {
        console.log("No more flashcards");
        // TODO
        return
    }

    flashcardIndex += 1;
    flip();
    displayFlashcard(flashcards);
}

function notLearned(flashcards) {
    // If current flashcard is the last one, do something
    if (flashcardIndex === flashcards.length - 1) {
        console.log("No more flashcards");
        // TODO
        return
    }

    flashcardIndex += 1;
    flip();
    displayFlashcard(flashcards);
}
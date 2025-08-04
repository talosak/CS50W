// This has to be a global variable
var flashcardIndex = 0;
var flashcards = [];
var remainingFlashcards = [];

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
    .then(responseFlashcards => {
        flashcards = responseFlashcards.splice(0);
        document.querySelector("#learnedButton").addEventListener('click', () => learned());
        document.querySelector("#notLearnedButton").addEventListener('click', () => notLearned());
        displayFlashcard();
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

function displayFlashcard() {
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

function learned() {
    // If current flashcard is the last one, shuffle and reset remaining flashcards
    if (flashcardIndex === flashcards.length - 1) {
        flashcards = remainingFlashcards.splice(0);
        remainingFlashcards = [];
        flashcardIndex = 0;
        flip();
        if (parseInt(flashcards.length) === 0) {
            alert("All learned");
            return
        }
        flashcards = shuffle(flashcards);
        displayFlashcard();
        return
    }

    flashcardIndex += 1;
    flip();
    displayFlashcard();
}

function notLearned() {
    // If current flashcard is the last one, shuffle and reset remaining flashcards
    if (flashcardIndex === flashcards.length - 1) {
        remainingFlashcards.push(flashcards[flashcardIndex]);
        flashcards = remainingFlashcards.splice(0);
        remainingFlashcards = [];
        flashcardIndex = 0;
        flip();
        flashcards = shuffle(flashcards);
        displayFlashcard();
        return
    }

    remainingFlashcards.push(flashcards[flashcardIndex]);
    flashcardIndex += 1;
    flip();
    displayFlashcard();
}

function shuffle(array) {
    let shuffledArray = [];
    while(true) {
        let index = Math.floor(Math.random() * array.length);
        if (!shuffledArray.includes(array[index])) {
            shuffledArray.push(array[index]);
        }
        if (shuffledArray.length === array.length) {
            return shuffledArray;
        }
    }
}
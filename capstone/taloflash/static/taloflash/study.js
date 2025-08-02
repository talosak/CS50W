document.addEventListener('DOMContentLoaded', () => {
    var flashcardFront = document.querySelector("#flashcardFront");
    var flashcardBack = document.querySelector("#flashcardBack");
    // TODO
});

function flip() {
    flashcardFront.classList.add("d-none")
    flashcardBack.classList.remove("d-none")
}
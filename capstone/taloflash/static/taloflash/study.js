document.addEventListener('DOMContentLoaded', () => {
    var flashcardFront = document.querySelector("#flashcardFront");
    var flashcardBack = document.querySelector("#flashcardBack");
    let pathnameArray = window.location.pathname.split("/");
    const flashset_id = pathnameArray[2];

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
    })
});

function flip() {
    flashcardFront.classList.add("d-none")
    flashcardBack.classList.remove("d-none")
}
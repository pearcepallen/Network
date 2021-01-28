document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new_post').addEventListener('submit', new_form);
});

function new_form() {
    fetch('/new_post',{
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#post').value
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
}


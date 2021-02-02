document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#new_post').addEventListener('submit', new_form);  
});


function new_form() {
    const form = document.querySelector('#new_post');
    csrftoken = form.getElementsByTagName('input')[0].value;
    fetch('/new_post',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
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


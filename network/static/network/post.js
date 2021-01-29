document.addEventListener('DOMContentLoaded', function() {
    posts();
});

function posts() {
    // Load Posts
    fetch('/posts')
        .then(response => response.json())
        .then(post => {
            // Print posts
            console.log(post);
        })
}


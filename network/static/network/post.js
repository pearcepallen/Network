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

            post.forEach(p => {
                const post_info = document.createElement('div');
                post_info.innerHTML = ('<div>' + `User: ${p.username}` + '</div>' 
                                        + '<div>' + `${p.content}` + '</div>' 
                                        + '<div>' + `${p.timestamp}` + '</div>'
                                        + '<div>' + `Likes: ${p.like}` + '</div>');
                document.querySelector('#posts').append(post_info);
            })
        })
}


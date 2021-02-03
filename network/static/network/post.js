document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#posts'))
    {
        posts();
    }
    if(document.querySelector('#profile'))
    {
        var user = document.querySelector('h1').innerHTML;
        profile(user);
    }
    
});

function posts() {
    // Load Posts
    fetch('/posts')
        .then(response => response.json())
        .then(post => {
            // Print posts
            console.log(post);

            post.forEach(p => {
                // Add User div and link
                const user = document.createElement('div');
                user.className = 'user';
                //user.innerHTML = `${p.username}`;
                const a = document.createElement('a');
                a.innerHTML = `${p.username}`;
                a.href = `/profile/${p.username}`;
                user.append(a);

                //Add content div
                const content = document.createElement('div');
                content.className = 'user';
                content.innerHTML = `${p.content}`;
                content.addEventListener('click', function() {
                    console.log(`${p.content} was clicked`);
                });

                //Add time div
                const time = document.createElement('div');
                time.className = 'user';
                time.innerHTML = `${p.timestamp}`;
                time.addEventListener('click', function() {
                    console.log(`${p.timestamp} was clicked`);
                });

                //Add likes div
                const like = document.createElement('div');
                like.className = 'user';
                like.innerHTML = `Likes: ${p.like}`;
                like.addEventListener('click', function() {
                    console.log(`Like ${p.like} was clicked`);
                });

                //innerHTML destroys child elements
                // Add a post div with previous children divs
                const post_info = document.createElement('div');
                post_info.className = "single_post";
                post_info.append(user);
                post_info.append(content);
                post_info.append(time);
                post_info.append(like);
                document.querySelector('#posts').append(post_info);
            })
        })
}

function profile(user) {
    // Load user posts
    fetch(`/posts/${user}`)
        .then(response => response.json())
        .then(posts => {    
            console.log(posts);
        });
}
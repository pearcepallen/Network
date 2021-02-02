document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#posts'))
    {
        posts();
    }
    /*if(document.querySelector('#profile'))
    {
        profile();
    }*/
    
});

function posts() {
    // Load Posts
    fetch('/posts')
        .then(response => response.json())
        .then(post => {
            // Print posts
            console.log(post);

            post.forEach(p => {

                const user = document.createElement('div');
                user.className = 'user';
                user.innerHTML = `${p.username}`;
                user.addEventListener('click', function() {
                    console.log(`${p.username} was clicked`);
                    window.location.replace = `profile/${p.username}`;
                    profile(`${p.username}`);
                });

                const content = document.createElement('div');
                content.className = 'user';
                content.innerHTML = `${p.content}`;
                content.addEventListener('click', function() {
                    console.log(`${p.content} was clicked`);
                });

                const time = document.createElement('div');
                time.className = 'user';
                time.innerHTML = `${p.timestamp}`;
                time.addEventListener('click', function() {
                    console.log(`${p.timestamp} was clicked`);
                });

                const like = document.createElement('div');
                like.className = 'user';
                like.innerHTML = `Likes: ${p.like}`;
                like.addEventListener('click', function() {
                    console.log(`Like ${p.like} was clicked`);
                });

                //innerHTML destroys child elements
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
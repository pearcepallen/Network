document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#posts'))
    {
        posts();
    }

    if(document.querySelector('#following'))
    {
        following();
    }

    if(document.querySelector('#profile'))
    {
        var user = document.querySelector('#profile_user').innerHTML;
        profile(user);

        var follow_button = document.querySelector('#follow_button')
        if(follow_button){
            fetch(`/following/${user}/${curr_user}`)
                .then(response => response.json())
                .then(response => {
                    follow_button.innerHTML = (response.follow === true? 'Unfollow' : 'Follow');
                });
            
            follow_button.addEventListener('click', () => {
                follow(user);
            });
        }
    }
});


function posts() {
    // Load Posts
    fetch('/posts')
        .then(response => response.json())
        .then(post => {
            // Print posts
            console.log(post);

            load_posts(post, '#posts');
        });
}

function following() {
    fetch(`/following_posts/${curr_user}`)
        .then(response => response.json())
        .then(post => {
            console.log(post);

            load_posts(post, '#following');
        })
}


function profile(user) {
    // Load user posts
    fetch(`/posts/${user}`)
        .then(response => response.json())
        .then(posts => {    
            console.log(posts);

            load_posts(posts, '#profile');
        });
}


function follow(user) {
    //Follow or Unfollow
    fetch(`/follow/${user}/${curr_user}`)
        .then(response => response.json())
        .then(result => { 
            console.log(result);
        });
}


function load_posts(post, page) {
    post.forEach(p => {
        // Add User div and link
        const user = document.createElement('div');
        user.className = 'user';
        //Add a tag
        const a = document.createElement('a');
        a.innerHTML = `${p.username}`;
        a.href = `/profile/${p.username}`;
        user.append(a);

        //Add content div
        const content = document.createElement('div');
        content.className = 'user';
        content.innerHTML = `${p.content}`;

        //Add time div
        const time = document.createElement('div');
        time.className = 'user';
        time.innerHTML = `${p.timestamp}`;

        //Add likes div
        const like = document.createElement('div');
        like.className = 'user';
        like.innerHTML = `Likes: ${p.like}`;
    
        //innerHTML destroys child elements
        // Add a post div with previous children divs
        const post_info = document.createElement('div');
        post_info.className = "single_post";
        post_info.append(user);
        post_info.append(content);
        post_info.append(time);
        post_info.append(like);
        document.querySelector(page).append(post_info);
    })
}
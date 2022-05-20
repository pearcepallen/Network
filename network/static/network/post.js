document.addEventListener('DOMContentLoaded', function() {
    if(document.querySelector('#posts'))
    {
        posts(1);
    }

    if(document.querySelector('#following'))
    {
        following(1);
    }

    if(document.querySelector('#profile'))
    {
        var user = document.querySelector('#profile_user').innerHTML;
        profile(user, 1);

        // Follower Count
        follower_count(user);
        
        // Following Count
        following_count(user);
        

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

// curr_user is user currently signed in

var posts_prev = false, posts_next = false;
function posts(page) {
    // Load Posts
    fetch(`/posts/${page}`)
        .then(response => response.json())
        .then(post => {
            // Print posts
            console.log(post.data);

            document.querySelector('#posts').innerHTML="";
            load_posts(post.data, '#posts');
            
            if(post.prev === null)
            {
                document.querySelector('#prev').style.display = 'none';
            }
            else
            {
                document.querySelector('#prev').style.display = 'block';
                if(posts_prev === false)
                {
                    document.querySelector('#prev').addEventListener('click', () => posts(page-1));
                    posts_prev = true;
                }      
            }

            if(post.next === null)
            {
                document.querySelector('#next').style.display = 'none';
            }
            else
            {
                document.querySelector('#next').style.display = 'block';
                if(posts_next === false)
                {
                    document.querySelector('#next').addEventListener('click', () => posts(page+1)); 
                    posts_next = true; 
                } 
            }
        });
}


function following(page) {
    fetch(`/following_posts/${curr_user}/${page}`)
        .then(response => response.json())
        .then(post => {
            document.querySelector('#following').innerHTML="";
            load_posts(post.data, '#following');

            if(post.prev === null)
            {
                document.querySelector('#prev').style.display = 'none';
            }
            else
            {
                document.querySelector('#prev').style.display = 'block';
                if(posts_prev === false)
                {
                    document.querySelector('#prev').addEventListener('click', () => posts(page-1));
                    posts_prev = true;
                }      
            }

            if(post.next === null)
            {
                document.querySelector('#next').style.display = 'none';
            }
            else
            {
                document.querySelector('#next').style.display = 'block';
                if(posts_next === false)
                {
                    document.querySelector('#next').addEventListener('click', () => posts(page+1)); 
                    posts_next = true; 
                } 
            }
        })
}


function profile(user, page) {
    // Load user posts
    fetch(`/posts/${user}/${page}`)
        .then(response => response.json())
        .then(post => {    
            console.log(post.data);

            document.querySelector('#profile').innerHTML="";
            load_posts(post.data, '#profile');

            if(post.prev === null)
            {
                document.querySelector('#prev').style.display = 'none';
            }
            else
            {
                document.querySelector('#prev').style.display = 'block';
                if(posts_prev === false)
                {
                    document.querySelector('#prev').addEventListener('click', () => posts(page-1));
                    posts_prev = true;
                }      
            }

            if(post.next === null)
            {
                document.querySelector('#next').style.display = 'none';
            }
            else
            {
                document.querySelector('#next').style.display = 'block';
                if(posts_next === false)
                {
                    document.querySelector('#next').addEventListener('click', () => posts(page+1)); 
                    posts_next = true; 
                } 
            }
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


function update_like(post, user) {
    //Like or unlike a post
    fetch(`/like/${post}/${user}`)
        .then(response => response.json())
        .then(result => { 
            return result
        });
}

function load_posts(post, page) {
    post.forEach(p => {
        var likes = 0;
        
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

        //Add like button
        const like_button = document.createElement('button');
        like_button.className = 'like-button';
        like_button.innerHTML = 'Like';
        like_button.onclick = update_like(p.id, curr_user);
        // var test = update_like(p.id, curr_user);
        // console.log(test);
        /*.then(
                function(value) {console.log(`Testing return value ${value.message}`);},
                function(error) {console.log(`Error: ${error}`)},
            );*/
    
        //innerHTML destroys child elements
        // Add a post div with previous children divs
        const post_info = document.createElement('div');
        post_info.className = "single_post";
        post_info.append(user);
        post_info.append(content);
        post_info.append(time);
        post_info.append(like);
        post_info.append(like_button);
        document.querySelector(page).append(post_info);
    })
    
    
}

function following_count(user) {
    //Follow or Unfollow
    fetch(`/following_count/${user}`)
        .then(response => response.json())
        .then(result => { 
            console.log(result.data)
            document.querySelector('#following_count').innerHTML += " " + result.data;
        });
}

function follower_count(user) {
    //Follow or Unfollow
    fetch(`/follower_count/${user}`)
        .then(response => response.json())
        .then(result => { 
            console.log(result.data);
            document.querySelector('#follower_count').innerHTML += " " + result.data;
        });
    
}

// function get_likes(post) {
//     fetch(`/like/${post}`)
//         .then(response => response.json)
// }


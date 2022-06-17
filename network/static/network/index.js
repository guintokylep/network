document.addEventListener('DOMContentLoaded', function() {
    display_post();
});

function addPost(){

        let body = document.querySelector('#addNewPost').value;

        let posts = new Object();
        posts.body = body;

        fetch('/posts', {
            method: 'POST',
            body: JSON.stringify(posts)
          })
          .then(response => response.json())
          .then(result => {
            
          });

          display_post();
}
function display_post(){

    const allPostsDiv = document.querySelector('#allPosts');

    var action = "allposts"
    fetch(`posts/${action}`)
    .then(response => response.json())
    .then(postsDisplay => {
        postsDisplay.forEach(element => {

            const div = document.createElement('div');
            div.setAttribute('id','posts');
            const h4 = document.createElement('h4');
            const a = document.createElement('a');
            const p1 = document.createElement('p');
            const p2 = document.createElement('p');
            p1.setAttribute('id','date');
            p2.setAttribute('id','content');

            a.setAttribute('href',`profile/${element.postUserId}`);
            a.innerHTML = element.postUser;
            h4.append(a);
            p1.innerHTML = element.date;
            p2.innerHTML = element.postDescription;
            div.append(h4);
            div.append(p1);
            div.append(p2);

            allPostsDiv.append(div);
        })
    })
} 

function unfollow(){
    
    let following = document.getElementById("following");
    let dataset = following.getAttribute('data-id');

    fetch(`unfollow/${dataset}`)
    .then(response => response.json())
    .then(follow => {
        document.querySelector('.followersCount').innerHTML = follow.followers;
        document.querySelector('.buttonFollow').innerHTML = '';
        const buttonFollow = document.createElement('button');
        buttonFollow.setAttribute('class','btn btn-info');
        buttonFollow.setAttribute('data-id',dataset);
        buttonFollow.setAttribute('id','follow');
        buttonFollow.setAttribute('onclick','follow()');
        buttonFollow.innerHTML = 'Follow';
        document.querySelector('.buttonFollow').append(buttonFollow);

    })
}

function follow(){
    
    let follow = document.getElementById("follow");
    let dataset = follow.getAttribute('data-id');

    fetch(`follow/${dataset}`)
    .then(response => response.json())
    .then(following => {
        document.querySelector('.followersCount').innerHTML = following.followers;
        document.querySelector('.buttonFollow').innerHTML = '';
        const buttonFollow = document.createElement('button');
        buttonFollow.setAttribute('class','btn btn-info');
        buttonFollow.setAttribute('data-id',dataset);
        buttonFollow.setAttribute('id','following');
        buttonFollow.setAttribute('onclick','unfollow()');
        buttonFollow.innerHTML = 'Following';
        document.querySelector('.buttonFollow').append(buttonFollow);

    })
}


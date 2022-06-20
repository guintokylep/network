let pageNo = 1;
let postingCount = 0;
let noOfPostPerPage = 2;

document.addEventListener('DOMContentLoaded', function() {

    display_post(pageNo);
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

          display_post(pageNo);
}
function display_post(pageNo){

    var url = window.location.href
    url = url.split("/")
    const allPostsDiv = document.querySelector('#allPosts');
    if( url[4] !== undefined ){
        var action = url[4]
    }else{
        var action = "allposts"
    }
    
    fetch(`posts/${action}/page=${pageNo}`)
    .then(response => response.json())
    .then(postsDisplay => {
        postingCount = document.querySelector(".postingCount").innerHTML;

        if(postingCount != null && postsDisplay.length != undefined && postsDisplay.length > 0){
            document.getElementsByClassName("pagination")[0].style.visibility = "visible"; 
        }else if(postingCount != null){
            document.getElementsByClassName("pagination")[0].style.visibility = "hidden"; 
        }
        allPostsDiv.innerHTML = '';

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
function page(value){
    currentPage = pageNo; 
    if(value === 'Next'){
        pageNo+= 1;
    }else if(value === 'Previous'){
        pageNo-= 1;
    }else{
        pageNo = parseInt(value);
    }
    
    if(pageNo > 1){
        document.querySelector('#previous').classList.remove("disabled");
    }else{
        document.querySelector('#previous').classList.add("disabled");
    }

    //page number active 
    if( pageNo > 2 || value == 2 && currentPage == 3 || value === 'Previous' && pageNo == 2 ){
        let elements = document.querySelectorAll('.pagination > li');
        let parent = document.querySelector('.pagination');
        elements[4].remove()
        elements[3].remove()
        elements[2].remove()
        elements[1].remove()

        const firstLiElem = document.createElement('li');
        firstLiElem.setAttribute('class','page-item')
        const firstElem = document.createElement('input');
        firstElem.setAttribute('type','button')
        firstElem.setAttribute('class', 'page-link')
        firstElem.setAttribute('onclick','page(this.value)')
        firstElem.setAttribute('value',pageNo-1)
        firstLiElem.append(firstElem)
        parent.append(firstLiElem)

        const secLiElem = document.createElement('li');
        secLiElem.setAttribute('class','page-item active')
        const secElem = document.createElement('input');
        secElem.setAttribute('type','button')
        secElem.setAttribute('class', 'page-link')
        secElem.setAttribute('onclick','page(this.value)')
        secElem.setAttribute('value',pageNo)
        secLiElem.append(secElem)
        parent.append(secLiElem)

        const thirdLiElem = document.createElement('li');
        thirdLiElem.setAttribute('class','page-item')
        if(Math.ceil(lastPage) == pageNo){  
            thirdLiElem.setAttribute('class','page-item disabled')
        }
        const thirdElem = document.createElement('input');
        thirdElem.setAttribute('type','button')
        thirdElem.setAttribute('class', 'page-link')
        thirdElem.setAttribute('onclick','page(this.value)')
        thirdElem.setAttribute('value',pageNo+1)
        thirdLiElem.append(thirdElem)
        parent.append(thirdLiElem)

        const nextLiElem = document.createElement('li');
        nextLiElem.setAttribute('class','page-item')
        nextLiElem.setAttribute('id','next')
        const nextElem = document.createElement('input');
        nextElem.setAttribute('type','button')
        nextElem.setAttribute('class', 'page-link')
        nextElem.setAttribute('onclick','page(this.value)')
        nextElem.setAttribute('value','Next')
        nextLiElem.append(nextElem)
        parent.append(nextLiElem)

    }else if(value === 'Next'){
        let elements = document.querySelectorAll('.pagination > li');

        elements[pageNo-1].classList.remove('active')
        elements[pageNo].classList.add('active')
    }

    if(value === 'Previous' && pageNo == 1 ){
        let elements = document.querySelectorAll('.pagination > li');

        elements[2].classList.remove('active')
        elements[1].classList.add('active')
    }

    if( value == 2 && currentPage == 1 ){
        let elements = document.querySelectorAll('.pagination > li');

        elements[1].classList.remove('active')
        elements[2].classList.add('active')
    }else if ( value == 1 ){
        let elements = document.querySelectorAll('.pagination > li');

        elements[2].classList.remove('active')
        elements[1].classList.add('active')
    }
    

    
    lastPage =  postingCount / noOfPostPerPage;
    
    if(Math.ceil(lastPage) != pageNo){
        document.querySelector('#next').classList.remove("disabled");
    }else{
        document.querySelector('#next').classList.add("disabled");
    }

    display_post(pageNo);
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


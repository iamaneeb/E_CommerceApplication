let thumbnails = document.getElementsByClassName('thumbnail');
let activeClass = document.getElementsByClassName('active');


for(var i=0;i<thumbnails.length;i++){
    thumbnails[i].addEventListener('mouseover',function(){
        // if there is more than 0 class name active remove it
        if(activeClass.length > 0){
            activeClass[0].classList.remove('active')
        }
        this.classList.add('active');
        document.getElementById('featured').src = this.src
    })
}

let Buttonleft = document.getElementById('button-left');
let Buttonright = document.getElementById('button-right');


Buttonleft.addEventListener('click',function(){
    document.getElementById('slider').scrollLeft -=180;
})

Buttonright.addEventListener('click',function(){
    document.getElementById('slider').scrollLeft +=180;
})

function submitForm() {
    document.getElementById("searchForm").submit();
}

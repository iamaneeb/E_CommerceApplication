document.addEventListener('DOMContentLoaded', function () {
    const imagegallery = document.getElementsByClassName('thumbnail');
    const activeimagegallery = document.getElementsByClassName('active');

    for (var i = 0; i < imagegallery.length; i++) {
        imagegallery[i].addEventListener('mouseover', function () {
            if (activeimagegallery.length > 0) {
                activeimagegallery[0].classList.remove('active');
            }

            this.classList.add('active');
            document.getElementById('featured').src = this.src;
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const Buttonleft = document.getElementById('button-left');
    const Buttonright = document.getElementById('button-right');


    Buttonleft.addEventListener('click',function(){
        document.getElementById('slider').scrollLeft -=180;
    })

    Buttonright.addEventListener('click',function(){
        document.getElementById('slider').scrollLeft +=180;
    })
})


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('registrationForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Use the reset() function to clear all input fields in the form
        const form = document.getElementById('registrationForm');
        form.reset();

        // Now you can submit the form
    });
})


    setTimeout(function () {
        $('#message').fadeIn('slow')
    }, 4000);
    function Hide(){
        var mess =document.getElementById('message').classList;
        mess.add('hide_message');
    }
    
function togglefuntion() {
    var gettingthemenuid = document.getElementById("menuscrollid");
    gettingthemenuid.classList.toggle("menushow");
}

// slide image\

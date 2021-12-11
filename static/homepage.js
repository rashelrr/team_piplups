function readReviews() {
    var restaurant = document.getElementById('restaurant').value;
    var allstars = document.getElementsByName('stars');
    var stars = '';
    for (var i = 0; i < allstars.length; i++) {
        var button = allstars[i];
        if (button.checked) {
            stars = button.value;
        }
    }

    var url;
    const Http =  new XMLHttpRequest();
    url = "http://127.0.0.1:5000/readreviews?restaurant=" + restaurant + "&stars=" + stars;         
    
    const finalurl = url;
    window.location.href = finalurl;
}

function login() {
    const Http =  new XMLHttpRequest();
    var  url = "http://127.0.0.1:5000/login"
    
    const finalurl = url;
    window.location.href = finalurl;
}

function addReview() {
    const Http =  new XMLHttpRequest();
    var  url = "http://127.0.0.1:5000/preaddreview"
    
    const finalurl = url;
    window.location.href = finalurl;
}

function editReview() {
    var url;
    const Http =  new XMLHttpRequest();
    url = "http://127.0.0.1:5000/editreview"
    
    const finalurl = url;
    window.location.href = finalurl;
}

function signup() {
    var url;
    const Http =  new XMLHttpRequest();
    url = "http://127.0.0.1:5000/signup"
    
    const finalurl = url;
    window.location.href = finalurl;
}

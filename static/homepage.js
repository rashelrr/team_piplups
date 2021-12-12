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

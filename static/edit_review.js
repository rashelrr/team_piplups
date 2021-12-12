function handleEditReview() {
    var restaurant = document.getElementById('restaurant').value;
    var review = document.getElementById('review').value;

    var allstars = document.getElementsByName('stars');
    var stars = '';
    for (var button in allstars) {
        if (button.checked) {
            stars = button.value;
        }
    }

    // check none of the fields are empty
    var url;
    const Http =  new XMLHttpRequest();
    if (restaurant == '' || stars == '' || review == '') {
        url = "http://127.0.0.1:5000/editreview";
    } else {
        url = "http://127.0.0.1:5000/editreview?restaurant=" + restaurant + "&stars=" + stars + "&review=" + review;        
    }
    const finalurl = url;
    window.location.href = finalurl;
}

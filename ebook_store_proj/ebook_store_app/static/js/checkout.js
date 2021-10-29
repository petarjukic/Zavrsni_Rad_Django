var form = document.getElementById('form');
csrftoken = form.getElementsByTagName("input")[0].value

document.getElementsByClassName('make-payment')[0].addEventListener('click', function(e){
    submitFormData();
});

function submitFormData() {
    var userFormData = {
        'username':null,
        'email':null,
        'total':total,
    };

    var shippingInfo = {
        'adress':null,
        'city':null,
        'country':null,
        'zip_code':null
    };

    if(user == 'AnonymousUser') {
        userFormData.username = form.username.value;
        userFormData.email = form.email.value;
    }
    
    shippingInfo.adress = form.adress.value;
    shippingInfo.city = form.city.value;
    shippingInfo.country = form.country.value;
    shippingInfo.zip_code = form.zip_code.value;

    
    var url = '/process-order/';
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
    })
    .then((response) => response.json())
    .then((data) => {
        alert('Order completed');
        cart = {};
        document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
        window.location.href = "/payment";
    })
}
window.onscroll = function() {myFunction()};
            
var header = document.getElementById("test");
var sticky = header.offsetTop;

function myFunction() {
    if (window.pageYOffset > sticky) {
    header.classList.add("sticky");
    } else {
    header.classList.remove("sticky");
    }
}

var updateBtns = document.getElementsByClassName('update-cart');

for(var i = 0; i < updateBtns.length; i++) { 
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action

        if(user == 'AnonymousUser') {
            addCookieItem(productId, action);
        }
        else {
            updateUserOrder(productId, action);
        }
    });
}

function addCookieItem(productId, action) {
    if(action == 'add') {
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity':1};
        }
        else {
            cart[productId]['quantity'] += 1;
        }
    }

    if(action == 'remove') {
        cart[productId]['quantity'] -= 1;

        if( cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/" ;
    location.reload();
}

function updateUserOrder(productId, action) {
    var url = '/update-item/';

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken  
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload();
    })
}
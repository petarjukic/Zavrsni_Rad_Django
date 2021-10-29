var stripe = Stripe('pk_test_51Ikr4mC7F1L551l3PB5ehcXUJD2RQESclILNK6RUgiEi2ep9TEAvyUW83zeVfGBcN5XB9qntEH4SQEoiTkQRl3Kf00fE4v0imp');
  
var elements = stripe.elements();
var card = elements.create('card');
var cardElement = elements.getElement('card');

card.mount('#card-element');

card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      stripeTokenHandler(result.token);
    }
  });
});

function stripeTokenHandler(token) {
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  form.submit();
}
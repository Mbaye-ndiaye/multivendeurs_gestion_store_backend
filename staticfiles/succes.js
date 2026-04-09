const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
console.log("queryString: ", queryString);
console.log("id: ", queryString.substring(1));
const order = urlParams.get("order");
console.log("order ", order);
// Get Stripe publishable key
fetch("/paid/" + order + "/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    console.log(data);
    // Redirect to Stripe Checkout
  })
  .then((res) => {
    console.log(res);
  });

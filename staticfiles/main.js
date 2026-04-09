console.log("Sanity check!");
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const total = urlParams.get("total");
const order = urlParams.get("order");

console.log("sssss: ", order);
console.log("total: ", total);
url = "/config/" + order + "/";
console.log("url", url);
// Get Stripe publishable key
fetch(url)
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    console.log("data", data);
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);
    //console.log("sss",total)

    // new
    // Event handler

    // document.getElementById("submitBtn").className = "button is-loading";
    // Get Checkout Session ID
    fetch("/create-checkout-session/" + total + "/" + order + "/")
      .then((result) => {
        return result.json();
      })
      .then((data) => {
        console.log("data", data);
        // Redirect to Stripe Checkout
        return stripe.redirectToCheckout({ sessionId: data.sessionId });
      })
      .then((res) => {
        console.log("dfpdfpdfop", res);
      });
  });

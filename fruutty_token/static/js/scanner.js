// script.js file

function domReady(fn) {
	if (
		document.readyState === "complete" ||
		document.readyState === "interactive"
	) {
		setTimeout(fn, 1000);
	} else {
		document.addEventListener("DOMContentLoaded", fn);
	}
}

domReady(function () {

	// If found you qr code
	function onScanSuccess(decodeText, decodeResult) {
		alert("You Qr is : " + decodeText, decodeResult);
    var myClasses = document.getElementsByClassName("results");


for (var i = 0; i < myClasses.length; i++) {
  myClasses[i].innerHTML = decodeText;
  document.getElementById('token_data').value = decodeText ;
  var json_fruuty = document.getElementById('token_data').value;
  const obj = JSON.parse(json_fruuty);
  document.getElementById('token_test').value = json_fruuty ;
  document.getElementById('token_check').value = obj.user_country;

  document.getElementById("store_name").innerHTML = 'shopt name     :' +  obj.store_name;
  document.getElementById("user_id").innerHTML = 'user  :   ' + obj.user_id;
  document.getElementById("token_id").innerHTML = 'token id :   ' + obj.token_id;
  document.getElementById("token_type").innerHTML = 'token type :   ' + obj.token_type;
  document.getElementById("product_name").innerHTML = 'product name :   ' + obj.product_name;
  document.getElementById("city").innerHTML = 'city :   ' + obj.city;
  document.getElementById("user_country").innerHTML = 'user country :   ' + obj.user_country;
  document.getElementById("trade_country").innerHTML = 'trade country   :   ' + obj.trade_country;
  document.getElementById("date").innerHTML = 'date :   ' + obj.date;
  document.getElementById("processor").innerHTML = 'processor   :   ' + obj.processor;
  document.getElementById("token_amount").innerHTML = 'amount   :   ' + obj.token_amount;


  }
	}

	let htmlscanner = new Html5QrcodeScanner(
		"my-qr-reader",
		{ fps: 10, qrbos: 250 }
	);
	htmlscanner.render(onScanSuccess);
});

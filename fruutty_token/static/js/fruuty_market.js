let carousel = document.querySelector('.carousel');
let cellCount = 5;
let selectedIndex = 0;

function rotateCarousel() {
  let angle = selectedIndex / cellCount * -360;
  carousel.style.transform = 'translateZ(-275px) rotateY(' + angle + 'deg)';
}

let prevButton = document.querySelector('.previous-button');
prevButton.addEventListener( 'click', function() {
  selectedIndex--;
  rotateCarousel();
});

let nextButton = document.querySelector('.next-button');
nextButton.addEventListener( 'click', function() {
  selectedIndex++;
  rotateCarousel();
});

//--------------//
// IMAGE TOGGLE //
//--------------//
function changeImage() {
// alert("click!");
	let x = document.getElementById("image");
	let y = document.getElementById("imageChangeButton");
	let cat_url = "https://cdn.shopify.com/s/files/1/1453/9306/products/19950NBT2-2_1024x1024.jpg?v=1504778561";
	let dog_url = "https://i.ebayimg.com/images/g/0z8AAOSwFe5Xz-p2/s-l300.jpg";
	if(x.src === cat_url){
	  x.src = dog_url;
	  y.innerText = "Change to Cat";
	} else {
	  x.src = cat_url;
	  y.innerText = "Change to Dog";
	}
}
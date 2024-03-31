
var upButtons = document.querySelectorAll('.up');

upButtons.forEach(button => {
  button.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
});

window.addEventListener('scroll', () => {
  upButtons.forEach(button => {
    if (window.pageYOffset > 200) {
      button.style.visibility = 'visible';
    } else {
      button.style.visibility = 'hidden';
    }
  });
});




const incrementButtons = document.querySelectorAll(".increment");
const decrementButtons = document.querySelectorAll(".decrement");

incrementButtons.forEach((incrementButton) => {
  incrementButton.addEventListener("click", () => {
    const quantitySpan = incrementButton.parentNode.querySelector(".number");
    let quantity = parseInt(quantitySpan.innerText);
    quantity++;
    quantitySpan.innerText = quantity;
  });
});

decrementButtons.forEach((decrementButton) => {
  decrementButton.addEventListener("click", () => {
    const quantitySpan = decrementButton.parentNode.querySelector(".number");
    let quantity = parseInt(quantitySpan.innerText);
    if (quantity > 1) {
      quantity--;
      quantitySpan.innerText = quantity;
    }
  });
});

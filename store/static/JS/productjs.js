const slides = document.querySelectorAll('.slide');
var prevBtn = document.querySelector('.prev');
var nextBtn = document.querySelector('.next');
let currentSlide = 0;

function showSlide(slideNum) {
    slides[currentSlide].classList.remove('active');
    slides[slideNum].classList.add('active');
    currentSlide = slideNum;
}

prevBtn.addEventListener('click', function () {
    if (currentSlide === 0) {
        showSlide(slides.length - 1);
    } else {
        showSlide(currentSlide - 1);
    }
});

nextBtn.addEventListener('click', function () {
    if (currentSlide === slides.length - 1) {
        showSlide(0);
    } else {
        showSlide(currentSlide + 1);
    }
});

showSlide(0);

const decrementBtn = document.getElementById('decrement');
const incrementBtn = document.getElementById('increment');
const numberSpan = document.getElementById('number');

let number = 0;

decrementBtn.addEventListener('click', function () {

    if (number > 0) {
        number--;
        numberSpan.textContent = number;
    }
});

incrementBtn.addEventListener('click', function () {

    if (number < 100) {
        number++;
        numberSpan.textContent = number;
    }
});



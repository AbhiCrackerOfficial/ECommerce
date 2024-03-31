function dropdown(drop, show) {
    let p = document.getElementById(drop);
    document.getElementById(show).addEventListener("click", function () {
        if (p.style.display === "block") {
            p.style.display = "none";
        }
        else {
            p.style.display = "block";
        }
    });
}
dropdown("sign", "account");
dropdown("drop-down", "drop");
dropdown("menu", "dropmenu");
dropdown("addnav", "internalmenu");
document.getElementById("close").addEventListener("click", function () {
    document.getElementById("addnav").style.display = "none";
});

window.addEventListener("resize", function () {
    if (window.innerWidth > 840) {
        document.getElementById("addnav").style.display = "flex";
    }
    else {
        document.getElementById("addnav").style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    var slider = document.getElementById("slider");
    var slideCount = slider.querySelectorAll("ul li").length;
    var slideWidth = slider.querySelector("ul li").offsetWidth / (window.innerWidth / 100);
    var slideHeight = slider.querySelector("ul li").offsetHeight / (window.innerHeight / 100);
    var sliderUlWidth = slideCount * slideWidth;
    var intervalId;
    var activeDotIndex = 0;
    var dots = document.querySelectorAll(".dot");

    slider.style.width = slideWidth + "vw";
    slider.style.height = slideHeight + "vh";

    slider.querySelector("ul").style.width = sliderUlWidth + "vw";
    slider.querySelector("ul").style.marginLeft = -slideWidth + "vw";

    slider.querySelector("ul li:last-child").parentNode.insertBefore(
        slider.querySelector("ul li:last-child"),
        slider.querySelector("ul li:first-child")
    );

    function moveLeft() {
        var ul = slider.querySelector("ul");
        ul.style.left = slideWidth + "vw";
        ul.insertBefore(ul.querySelector("li:last-child"), ul.querySelector("li:first-child"));
        ul.style.left = "";
        activeDotIndex = (activeDotIndex - 1 + dots.length) % dots.length;
        updateActiveDot();
    }

    function moveRight() {
        var ul = slider.querySelector("ul");
        ul.style.left = -slideWidth + "vw";
        ul.appendChild(ul.querySelector("li:first-child"));
        ul.style.left = "";
        activeDotIndex = (activeDotIndex + 1) % dots.length;
        updateActiveDot();
    }

    function updateActiveDot() {
        for (var i = 0; i < dots.length; i++) {
            dots[i].classList.remove("active");
        }
        dots[activeDotIndex].classList.add("active");
    }


    dots.forEach(function (dot, index) {
        dot.addEventListener("click", function () {
            if (index > activeDotIndex) {
                var diff = index - activeDotIndex;
                for (var i = 0; i < diff; i++) {
                    moveRight();
                }
            } else if (index < activeDotIndex) {
                var diff = activeDotIndex - index;
                for (var i = 0; i < diff; i++) {
                    moveLeft();
                }
            }
        });
    });

    function autoSlide() {
        intervalId = setInterval(function () {
            moveRight();
            updateActiveDot();
        }, 2000);
    }

    autoSlide();

    slider.addEventListener("mouseenter", function () {
        clearInterval(intervalId);
    });

    slider.addEventListener("mouseleave", function () {
        autoSlide();
    });

});



var prevBtn = document.getElementById('prevBtn');
var nextBtn = document.getElementById('nextBtn');
var cardsContainer = document.querySelector('.cards-container');

prevBtn.addEventListener('click', () => {
    cardsContainer.style.transition = 'none';
    cardsContainer.insertBefore(cardsContainer.lastElementChild, cardsContainer.firstElementChild);
    cardsContainer.style.transform = 'translateX(-300px)';
    setTimeout(() => {
        cardsContainer.style.transition = 'transform 1s ease-in-out';
        cardsContainer.style.transform = 'translateX(0)';
    }, 100);
});

nextBtn.addEventListener('click', () => {
    cardsContainer.style.transition = 'none';
    cardsContainer.appendChild(cardsContainer.firstElementChild);
    cardsContainer.style.transform = 'translateX(300px)';
    setTimeout(() => {
        cardsContainer.style.transition = 'transform 1s ease-in-out';
        cardsContainer.style.transform = 'translateX(0)';
    }, 300);
});

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

function search() {
    // Get the form element and submit it
    const form = document.getElementById('search-form');
    form.submit();
}

// function filter(value) {
// }
// var radiobtns = document.getElementsByClassName('checkbox-item');
// let btnvalue = 9999999999;
// radiobtns.forEach(button => {
//     if (button.querySelector('input').checked) {
//         btnvalue = button.querySelector('input').value;
//     }
// });

// document.addEventListener('DOMContentLoaded', function () {
//     const filterform = document.getElementById('filter-form');
//     const priceradios = document.getElementsByName('price');
//     for (let i = 0; i < priceradios.length; i++) {
//         priceradios[i].addEventListener('change', function () {
//             filterform.sumbit();
//         })
//     }
// })

var dropdownToggle = document.getElementById("btn");
var dropdownMenu = document.getElementById("dropdown-menu");

dropdownToggle.addEventListener("click", () => {
    dropdownMenu.style.display === "none"
        ? dropdownMenu.style.display = "block"
        : dropdownMenu.style.display = "none";
});

var pagination = document.querySelector('.pagination');
var pages = pagination.querySelectorAll('.page');
var prev = pagination.querySelector('.prev');
var next = pagination.querySelector('.next');
var current = 0;

function showPage(page) {
    pages[current].classList.remove('active');
    pages[page].classList.add('active');
    current = page;
}

function prevPage() {
    if (current > 0) {
        showPage(current - 1);
    }
}

function nextPage() {
    if (current < pages.length - 1) {
        showPage(current + 1);
    }
}

prev.addEventListener('click', prevPage);
next.addEventListener('click', nextPage);

for (var i = 0; i < pages.length; i++) {
    pages[i].addEventListener('click', (function (i) {
        return function () {
            showPage(i);
        }
    })(i));
}

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


document.addEventListener('DOMContentLoaded', function() {
    const priceInputs = document.querySelectorAll('input[name="price"]');
    const filterForm = document.getElementById('filter-form');
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');

    priceInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min_price = parseInt(input.dataset.min, 10);
            const max_price = parseInt(input.dataset.max, 10);
            console.log("min_price:", min_price, "max_price:", max_price);

            // Update the hidden input fields with min_price and max_price
            minPriceInput.value = min_price;
            maxPriceInput.value = max_price;

            // Update the form action with the min_price and max_price URL parameters
            const currentUrl = new URL(window.location.href);
            const searchParams = currentUrl.searchParams;
            searchParams.delete('price'); // Remove the 'price' parameter
            searchParams.set('min_price', min_price);
            searchParams.set('max_price', max_price);
            currentUrl.search = searchParams.toString();
            window.location.href = currentUrl.toString();
        });
    });
});

function oppdaterKlokkeOgDato() {
    const now = new Date();
    // Tid
    const timeString = now.toLocaleTimeString('nb-NO', {
        hour: '2-digit',
        minute: '2-digit'
    });
    // Dato med ukedag og måned skrevet ut
    const options = { weekday: 'long', day: 'numeric', month: 'long' };
    const dateString = now.toLocaleDateString('nb-NO', options);
    document.getElementById('time').textContent = timeString;
    document.getElementById('date').textContent = dateString.charAt(0).toUpperCase() + dateString.slice(1);
}

function oppdaterVelkommen() {
    const now = new Date();
    const hour = now.getHours();
    let greeting = "God morgen";
    if (hour >= 12 && hour < 18) {
        greeting = "God ettermiddag";
    } else if (hour >= 18 || hour < 5) {
        greeting = "God kveld";
    }
    document.getElementById('greeting').textContent = greeting;
}

// Slideshow funksjonalitet
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const indicators = document.querySelectorAll('.indicator');
const totalSlides = slides.length;
let slideshowInterval = null;
let inSettings = false;

function visSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    slides[index].classList.add('active');
    indicators[index].classList.add('active');
}

function nesteSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    visSlide(currentSlide);
}

function forrigeSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    visSlide(currentSlide);
}

function startSlideshow() {
    if (slideshowInterval) clearInterval(slideshowInterval);
    slideshowInterval = setInterval(nesteSlide, 10000);
}

function stopSlideshow() {
    if (slideshowInterval) clearInterval(slideshowInterval);
}


window.onload = function() {
    oppdaterKlokkeOgDato();
    oppdaterVelkommen();
    setInterval(oppdaterKlokkeOgDato, 1000);
    setInterval(oppdaterVelkommen, 60000);

    startSlideshow();

    document.addEventListener('keydown', function(e) {
        if (!inSettings) {
            if (e.key === "ArrowRight") {
                nesteSlide();
            } else if (e.key === "ArrowLeft") {
                forrigeSlide();
            }
        }
    });

    document.getElementById('settingsBtn').onclick = åpneSettings;
};
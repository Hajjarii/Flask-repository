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

function åpneSettings() {
    inSettings = true;
    document.getElementById('settingsView').style.display = 'flex';
    document.getElementById('calendarView').style.display = 'none';
    stopSlideshow();
}

function lukkSettings() {
    inSettings = false;
    document.getElementById('settingsView').style.display = 'none';
    document.getElementById('calendarView').style.display = 'block';
    setTimeout(startSlideshow, 10000); // Vent 10 sekunder før slideshow starter igjen
}

function leggTilKalenderItem() {
    const title = document.getElementById('eventTitle').value;
    const time = document.getElementById('eventTime').value;
    
    if (title && time) {
        const calendarView = document.getElementById('calendarView');
        const newItem = document.createElement('div');
        newItem.className = 'calendar-item';
        newItem.innerHTML = `
            <div class="calendar-item-title">${title}</div>
            <div class="calendar-item-time">${time}</div>
            <button class="delete-btn" onclick="slettKalenderItem(this)">✕</button>
        `;
        calendarView.appendChild(newItem);
        
        document.getElementById('eventTitle').value = '';
        document.getElementById('eventTime').value = '';
        lukkSettings();
    } else {
        alert('Vennligst fyll inn både tittel og tid');
    }
}

function slettKalenderItem(btn) {
    btn.parentElement.remove();
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

document.getElementById('calendarView').addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-btn')) {
        e.target.parentElement.remove();
    }
});
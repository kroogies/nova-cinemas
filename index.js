// Hover Effects
document.getElementById("cmsoon").addEventListener("mouseenter", function() {
    if (!this.classList.contains("active")) {
        this.style.color = "#968469";  // Hover color
    }
});

document.getElementById("nshowing").addEventListener("mouseenter", function() {
    if (!this.classList.contains("active")) {
        this.style.color = "#968469";  // Hover color
    }
});

document.getElementById("cmsoon").addEventListener("mouseleave", function() {
    if (!this.classList.contains("active")) {
        this.style.color = "#e0e0e0";  // Default color
    }
});

document.getElementById("nshowing").addEventListener("mouseleave", function() {
    if (!this.classList.contains("active")) {
        this.style.color = "#e0e0e0";  // Default color
    }
});

// Click Events
document.getElementById("cmsoon").addEventListener("click", function() {
    document.getElementById("nwshowing_hr").style.left = '35.5%'; // Move the hr
    this.style.color = '#D6BD98';  // Active color for cmsoon
    document.getElementById("nshowing").style.color = '#e0e0e0';  // Reset color for nshowing
    this.classList.add("active"); // Mark as active
    document.getElementById("nshowing").classList.remove("active"); // Remove active from nshowing
});

document.getElementById("nshowing").addEventListener("click", function() {
    document.getElementById("nwshowing_hr").style.left = '18.3%'; // Move the hr
    this.style.color = '#D6BD98';  // Active color for nshowing
    document.getElementById("cmsoon").style.color = '#e0e0e0';  // Reset color for cmsoon
    this.classList.add("active"); // Mark as active
    document.getElementById("cmsoon").classList.remove("active"); // Remove active from cmsoon
});


const upcomingMovies = document.querySelectorAll('.coming-soon');
const movieListElements = document.querySelectorAll('.movie-list');
const buyTicketButton = document.querySelectorAll('#buy_ticket')

document.getElementById("cmsoon").addEventListener("click", function() {
    // Change the opacity for each element
    movieListElements.forEach(element => {
        element.style.opacity = '0%';
        element.style.zIndex = '1'
    });

    upcomingMovies.forEach(element => {
        element.style.opacity = '100%'
        element.style.zIndex = '2'
    })
})

document.getElementById("nshowing").addEventListener("click", function() {
    upcomingMovies.forEach(element => {
        element.style.opacity = '0%';
        element.style.zIndex = '1'
    });

    movieListElements.forEach(element => {
        element.style.opacity = '100%'
        element.style.zIndex = '2'
    })
})

document.querySelectorAll(".movie-container button").forEach(function(button) {
    button.addEventListener("click", function() {
        const movieName = this.parentElement.querySelector("h3").textContent.replace(/\s+/g, '-').toLowerCase();
        window.location.href = `/${movieName}`; // Directly use the movie slug
    });
});

document.querySelectorAll("#np_poster").forEach(function(button) {
    button.addEventListener("click", function() {
        const movieName = this.parentElement.querySelector("h3").textContent.replace(/\s+/g, '-').toLowerCase();
        window.location.href = `/${movieName}`; // Directly use the movie slug
    });
});

document.querySelectorAll("#web_lg").forEach(function(button) {
    button.addEventListener("click", function() {
        window.location.href = '/'; // Redirects to home page
    });
});

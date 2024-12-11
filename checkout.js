document.querySelectorAll("#web_lg").forEach(function(button) {
    button.addEventListener("click", function() {
        window.location.href = '/'; // Redirects to home page
    });
});

document.getElementById("showtimes_btn").addEventListener("click", function() {
    const movieSlug = "{{ movie_slug|escapejs }}"; // Escaping ensures proper handling of special characters
    window.location.href = `/${movieSlug}/checkout`; // Correct redirection
});

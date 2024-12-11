document.querySelectorAll("#web_lg").forEach(function(button) {
    button.addEventListener("click", function() {
        window.location.href = '/'; // Redirects to home page
    });
});

function increment() {
    let inputField = document.getElementById('ticket-quantity');
    if (parseInt(inputField.value) < 10) { // Check if value is less than 10
        inputField.value = parseInt(inputField.value) + 1;
        updateTicketCount(); // Sync the p tag
    }
}

function decrement() {
    let inputField = document.getElementById('ticket-quantity');
    if (parseInt(inputField.value) > 0) { // Check if value is greater than 0
        inputField.value = parseInt(inputField.value) - 1;
        updateTicketCount(); // Sync the p tag
    }
}

function updateTicketCount() {
    let inputField = document.getElementById('ticket-quantity');
    let ticketCount = document.getElementById('ticket_count');
    ticketCount.textContent = inputField.value; // Update p tag with the input value
}

document.getElementById("submitBTN").addEventListener("click", function(event) {
    let requiredFields = [
        document.getElementById('first_name'),
        document.getElementById('last_name'),
        document.getElementById('movie'),
        document.getElementById('cinema_number'),
        document.getElementById('screen_time'),
        document.getElementById('phone_number'),
        document.getElementById('address')
    ];

    let ticketQuantity = document.getElementById('ticket-quantity').value;
    let phoneNumber = document.getElementById('phone_number').value;

    // Check if all fields are filled
    let allFieldsFilled = requiredFields.every(function(field) {
        return field.value.trim() !== ""; // Ensure the field is not empty
    });

    // Check if ticket quantity is greater than 0
    let validTicketCount = parseInt(ticketQuantity) > 0;

    // Check if the phone number contains only 12 digits
    let validPhoneNumber = /^\d{11}$/.test(phoneNumber); // This ensures the phone number is exactly 12 digits

    if (!allFieldsFilled) {
        event.preventDefault(); // Prevent form submission
        alert("Please fill in all fields.");
        return;
    }

    if (!validTicketCount) {
        event.preventDefault(); // Prevent form submission
        alert("Please ensure the ticket count is greater than 0.");
        return;
    }

    if (!validPhoneNumber) {
        event.preventDefault(); // Prevent form submission
        alert("Please enter a valid phone number containing exactly 12 digits.");
        return;
    }

    if (allFieldsFilled && validTicketCount && validPhoneNumber) {
        // All conditions are met, execute your own logic here
        console.log("All conditions are met. Proceeding...");
        customLogic(); // Call your custom logic here
    }    
});

function customLogic() {
    let elements = document.querySelectorAll('.floor1');  // Select all elements with the class
    elements.forEach(function(element) {
        element.style.opacity = 0;
        element.style.zIndex = 1;
        element.style.pointerEvents = 'none';  // Disable interaction
    });

    let y = document.querySelectorAll('.floor2');  // Select all elements with the class
    y.forEach(function(element) {
        element.style.opacity = 1;
        element.style.zIndex = 5;
        element.style.pointerEvents = 'auto';  // Enable interaction
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const seats = document.querySelectorAll('.seat-container');

    seats.forEach(seat => {
        const seatImage = seat.querySelector('.seat-image'); // Select the <img> inside the seat-container

        // Handle hover effect
        seat.addEventListener('mouseover', function () {
            if (seatImage.dataset.status === 'available' && !seat.classList.contains('selected')) {
                seatImage.src = seatImage.dataset.hoverImage || '/static/images/on_hover.png'; // Hover image
            }
        });

        seat.addEventListener('mouseout', function () {
            if (!seat.classList.contains('selected')) {
                seatImage.src = seatImage.dataset.availableImage || '/static/images/available.png'; // Available image
            }
        });

        // Handle seat click
        seat.addEventListener('click', function () {
            if (seatImage.dataset.status === 'available') {
                // Toggle the 'selected' class on the clicked seat
                console.log("seat clicked");
                seat.classList.toggle('selected');

                // Change image after selection
                if (seat.classList.contains('selected')) {
                    seatImage.src = seatImage.dataset.selectedImage || '/static/images/selected.png'; // Selected image
                } else {
                    seatImage.src = seatImage.dataset.availableImage || '/static/images/available.png'; // Available image
                }
            }
        });
    });
});


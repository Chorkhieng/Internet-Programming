// function to remove current clicked row
function removeRow() {
    let table = document.getElementById("contact-table");
    let tbody = table.tBodies[0];

    tbody.addEventListener("click", function (event) {
        if (event.target.tagName === "BUTTON") {
            // Get the parent row of the clicked button
            let row = event.target.parentElement.parentElement;
            // Remove the row
            tbody.removeChild(row);
        }
    });
}


// function to calculate time until appointment dates
function timeUntilAppointments() {
    const appointmentDates = document.querySelectorAll(".appointment-date");
    appointmentDates.forEach(function (appointmentDate) {
        // to avoid updated times adding up to the previous time
        // keep the original appointment date
        // and update the calculated time to be the current time
        const appointmentDateString = appointmentDate.innerText.split(" - ")[0];
        let currentDate = new Date().getTime();
    
        // Parse the date string in "YYYY-MM-DD" format
        const parts = appointmentDateString.split('-');
        const year = parseFloat(parts[0]);
        const month = parseFloat(parts[1]) - 1;
        const day = parseFloat(parts[2]);
        const appointment = new Date(year, month, day);
    
        const time = appointment - currentDate;

        // check for past and future dates
        if (time < 0) {
            appointmentDate.innerText = appointmentDateString + " - Past"
        } else {
            const second = Math.floor(time / 1000);
            const minute = Math.floor(second / 60);
            const hour = Math.floor(minute / 60);
            const days = Math.floor(hour / 24);
    
            // Update the HTML element with the current time
            appointmentDate.innerText = appointmentDateString + " - " 
                                    + days + " days, " + (hour % 24) + " hours, " 
                                    + (minute % 60) + " minutes, " + (second % 60)
                                    + " seconds left"
        }
        
    });
}

// Wait until the full document is loaded
document.addEventListener("DOMContentLoaded", removeRow);
// set time interval for updating time until appointment 
setInterval(timeUntilAppointments, 1000);

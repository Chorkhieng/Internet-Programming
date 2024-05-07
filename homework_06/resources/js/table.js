
// that remove row permanently 
function removeRow() {
    let table = document.getElementById("contact-table");
    let tbody = table.tBodies[0];

    tbody.addEventListener("click", async (event) => {
        if (event.target.tagName === "BUTTON") {
            // Get the parent row of the clicked button
            const row = event.target.parentElement.parentElement;
            const id = parseInt(row["id"]);

            const result = await fetch("http://localhost:4131/api/contact", {
                method: "DELETE",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({"id": id})
            });

            // remove row from front-end
            if (result.status == 200 || result.status == 404) {
                tbody.removeChild(row);
            }
        }
    });
}


// function to calculate time until appointment dates
function timeUntilAppointments() {
    const appointmentDates = document.querySelectorAll(".appointment-date");
  
    appointmentDates.forEach((appointmentDate) => {
      const appointmentDateString = appointmentDate.innerText.split(" - ")[0];
      const currentDate = new Date().getTime();
  
      let appointment = new Date(appointmentDateString);
      let time = appointment - currentDate;
  
      if (isNaN(time)) {
        // If parsing with letters fails, try "YYYY-MM-DD" format
        const [year, month, day] = appointmentDateString.split('-');
        appointment = new Date(year, month - 1, day);
        time = appointment - currentDate;
      }
  
      if (time < 0) {
        appointmentDate.innerText = appointmentDateString + " - Past";
      } else {
        const second = Math.floor(time / 1000);
        const minute = Math.floor(second / 60);
        const hour = Math.floor(minute / 60);
        const days = Math.floor(hour / 24);
  
        // Update the HTML element with the current time
        appointmentDate.innerText = appointmentDateString + " - " +
          days + " days, " + (hour % 24) + " hours, " +
          (minute % 60) + " minutes, " + (second % 60) +
          " seconds left";
      }
    });
}

// Wait until the full document is loaded
document.addEventListener("DOMContentLoaded", removeRow);
// set time interval for updating time until appointment 
setInterval(timeUntilAppointments, 1000);

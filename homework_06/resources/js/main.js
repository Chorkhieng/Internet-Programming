// toggle switch for dark or norman mode
function toggleMode() {
    const mode = document.getElementById("dark-light");
    const changeMode = document.getElementById("css-mode");
    let isDarkMode = localStorage.getItem("isDarkMode") === "true";
  
    // switch between css files to change background colors
    // and change the text to indicate option (Dark Mode/ Light Mode)
    if (isDarkMode) {
      changeMode.setAttribute("href", "/css/main.css");
      mode.innerText = "Dark Mode";
      isDarkMode = false;
    } else {
      changeMode.setAttribute("href", "/css/main.dark.css");
      mode.innerText = "Light Mode";
      isDarkMode = true;
    }
  
    // Store the current theme mode in localStorage
    localStorage.setItem("isDarkMode", isDarkMode.toString());
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    const darkTheme = document.getElementById("dark-light");
    darkTheme.addEventListener("click", function (event) {
      event.preventDefault();
      toggleMode();
    });
  
    // Check for the initial theme mode and set it
    let isDarkMode = localStorage.getItem("isDarkMode") === "true";
    if (isDarkMode) {
      document.getElementById("css-mode").setAttribute("href", "/css/main.dark.css");
      document.getElementById("dark-light").innerText = "Light Mode";
    } else {
      document.getElementById("css-mode").setAttribute("href", "/css/main.css");
      document.getElementById("dark-light").innerText = "Dark Mode";
    }
  });
  
  
  // implementation for sale api
  // enble admin to create or delete sale's text
  // on the front-end
  function setSale() {
    const saleButton = document.getElementById("set-sale");
    const saleText = document.getElementById("input-sale");
    const confirmSale = document.getElementById("sale-change");
  
    saleButton.addEventListener("click", async () => {
      // Define the JSON payload for the POST request
      const postPayload = {
        "message": saleText.value
      };
  
      // Send a POST request to update the sale message
      const result = await fetch("http://localhost:4131/api/sale", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postPayload),
      })
      // confirmation message
      if (result.status === 200){
        confirmSale.innerHTML = "New sale has been added successfully!";
      }
    });
  }
  
  // delete sale text
  function endSale() {
    const saleButton = document.getElementById("end-sale");
    const saleText = document.getElementById("input-sale");
    const confirmSale = document.getElementById("sale-change");
  
    saleButton.addEventListener("click", async () => {
      // Define the JSON payload for the POST request
      const postPayload = {
        "message": saleText.value
      };
  
      // Send a POST request to update the sale message
      const result = await fetch("http://localhost:4131/api/sale", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postPayload),
      })
      // Display the message value from the JSON response in the HTML element
      if (result.status === 200) {
        confirmSale.innerText = "Sale has been deleted successfully!";
      }
    });
  }
  
  
  // get sale text to main page
  async function getSaleText() {
    const saleText = document.getElementById("sale-text");
    const response = await fetch("http://localhost:4131/api/sale", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    })
    const message = await response.json();
    if ("message" in message) {
      saleText.textContent = message["message"];
    }
    if (message["active"] == false) {
      saleText.innerText = "";
    }
  }
  
  document.addEventListener("DOMContentLoaded", setSale);
  document.addEventListener("DOMContentLoaded", endSale);
  // setInterval(setSale, 1000);
  // setInterval(endSale, 1000);

  // update sale get sale every second
  setInterval(getSaleText, 1000);
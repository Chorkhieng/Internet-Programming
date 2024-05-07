// set discount function 
let disc = 40;
function discount() {
    const mail = document.getElementById("email");
    // get more discount for students
    if (mail.value.indexOf(".edu") != -1) {
        disc = 100;
    }
}

// estimated price
function estimatePrice() {
    const price = document.getElementById("price-estimate");
    const choice = document.getElementById("choice");
    const chosenChoice = choice.value;

    if (chosenChoice === "personal") {
        price.innerText = "Estimated price per person: $" + (885 - disc);
    } else if (chosenChoice === "family") {
        price.innerText = "Estimated price per person: $" + (780 - disc);
    } else if (chosenChoice === "business") {
        price.innerText = "Estimated price per person: $" + (2500 - disc);
    } else if (chosenChoice === "VIP package") {
        price.innerText = "Estimated price per person: $" + (2900 - disc);
    } else {
        price.innerText = "Estimated price per person: $" + (885 - disc);
    }
}

// wait untill full document loaded
document.addEventListener("DOMContentLoaded", function() {
    let choose = document.getElementById("choice");
    let chooseMail = document.getElementById("email");

    choose.addEventListener("change", estimatePrice);
    chooseMail.addEventListener("change", discount);
});
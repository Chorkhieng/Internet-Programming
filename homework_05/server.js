// server file using expressjs
const express = require ('express');
const basicAuth = require('express-basic-auth')
const app = express();
const port = 4131;

app.set("views", "templates");
app.set("view engine", "pug");

// dummy data
const contacts = [
    {"id": 0, "first": "John", "email": "john@hismail.com", "bookDate": "2023-11-05", "translator": "no", "choice": "personal"},
    {"id": 1, "first": "Jane", "email": "jane@theirmail.com", "bookDate": "2023-01-06", "translator": "yes", "choice": "family"},
    {"id": 2, "first": "Jing", "email": "jlang@theirmail.com", "bookDate": "2023-12-08", "translator": "yes", "choice": "VIP package"}
];

// set id for contact
let ID = 3;

// dummy sale json
let sale = {"active": true, "message": "25% off every package"};

app.use(express.static('resources'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// basic authentication
const authenticate = basicAuth({
        users: { 'admin': 'password' },
        challenge: true,
        realm: 'User Visible Realm',
})


// middleware function
app.use((req, res, next)=> {
    console.log(req.method, `localhost:${port}${req.path}`);
    // run the actual request handler
    next();
    // console.log(req.method, `localhost:${port}${req.path}`, res.statusCode, res.statusMessage);
    console.log(res.statusCode, res.statusMessage);
})

// image file
app.get("/images/angkor.jpeg", (req, res)=>{
    res.send(`angkor.jpeg`);
})

// main page
app.get("/", (req, res)=>{
    res.render("mainpage.pug");
})

app.get("/main", (req, res)=>{
    res.render("mainpage.pug");
})

// testimonies page
app.get("/testimonies", (req, res)=>{
    res.render("testimonies.pug");
})

// contactform page
app.get("/contact", (req, res)=>{
    res.render("contactform.pug");
})

app.post("/contact", (req, res)=>{
    
    const data = req.body;
    if (!req.body) {
        res.status(400).render("unsuccess.pug");
    }
    else if (!data.first || !data.last || !data.bookDate || !data.email) {
        res.status(400).render("unsuccess.pug");
    }
    else {
        // make check box to get yes/no words
        if (data.translator == "on"){
            data.translator = "yes";
        }
        else {
            data.translator = "no";
        }
        if ((data.first === "") || (data.last === "") || (data.bookDate === "")
            || (data.email === "") || (data.choice === "")) {
            res.status(400).render("unsuccess.pug");
        }
        else if ((data.first.indexOf("&", 0) != -1) || (data.last.indexOf("&", 0) != -1) 
                || (data.first.indexOf("=", 0) != -1) || (data.last.indexOf("=", 0) != -1)){
            res.status(400).render("unsuccess.pug");
        }
        else {
            data.id = ID;
            ID += ID + 1;
            contacts.push(data);
            res.render("confirm_success.pug");
        }
    }
})

// delete contact(s) from contact list
app.delete("/api/contact", authenticate, (req, res)=>{
    if ("id" in req.body){
        for (const contact of contacts){
            if (req.body.id == contact.id) {
                const index = contacts.indexOf(contact);
                contacts.splice(index, 1);
            }
        }
        res.send(contacts);
    }
})

// contactlog page
app.get("/admin/contactlog", authenticate, (req, res)=>{
    res.render("contactlog.pug", {contacts:contacts});
})

// css files
app.get("/css/main.css", (req, res)=>{
    res.send("main.css");
})

app.get("/css/main.dark.css", (req, res)=>{
    res.render("main.dark.css");
})

// js files
app.get("/js/main.js", (req, res)=>{
    res.send("main.js");
})

app.get("/js/table.js", (req, res)=>{
    res.send("table.js");
})

app.get("/js/contact.js", (req, res)=>{
    res.send("contact.js");
})

// sale api
app.get("/api/sale", (req, res)=>{
    if (("active" in sale) && (sale.active == true)) {
        res.send(sale);
    }
    else {
        sale = {"active": false};
        res.send(sale);
    }
})

app.post("/api/sale", authenticate, (req, res)=>{
    sale.active = true;
    sale.message = req.body.message;
    res.send(sale);
})

app.delete("/api/sale", authenticate, (req, res)=>{
    sale = {"active": false};
    res.send(sale);
})

// 404 not found page
app.use((req, res) => {
    res.status(404).render("404.pug");
})

app.listen(port , () => {
    console.log(`Listening on port ${port}`);
})
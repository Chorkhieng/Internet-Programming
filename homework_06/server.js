// server file using expressjs
const express = require ('express');
const basicAuth = require('express-basic-auth');
const data = require('./data');
const app = express();
const port = 4131;

app.set("views", "templates");
app.set("view engine", "pug");


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
    // console.log(req.method, `localhost:${port}${req.path}`);
    // run the actual request handler
    next();
    console.log(req.method, `localhost:${port}${req.path}`, res.statusCode);
    // console.log(res.statusCode, res.statusMessage);
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

app.post("/contact", async (req, res)=>{
    
    const result = req.body;
    if (!req.body) {
        res.status(400).render("unsuccess.pug");
    }
    else if (!result.first || !result.last || !result.bookDate || !result.email) {
        res.status(400).render("unsuccess.pug");
    }
    else {
        // make check box to get yes/no words
        if (result.translator == "on"){
            result.translator = "yes";
        }
        else {
            result.translator = "no";
        }
        if ((result.first === "") || (result.last === "") || (result.bookDate === "")
            || (result.email === "") || (result.choice === "")) {
            res.status(400).render("unsuccess.pug");
        }
        else if ((result.first.indexOf("&", 0) != -1) || (result.last.indexOf("&", 0) != -1) 
                || (result.first.indexOf("=", 0) != -1) || (result.last.indexOf("=", 0) != -1)){
            res.status(400).render("unsuccess.pug");
        }
        else {
            await data.addContact(result);
            res.render("confirm_success.pug");
        }
    }
})

// delete contact(s) from contact list
app.delete("/api/contact", authenticate, async (req, res)=>{
    const contacts = await data.getContacts();
    if ("id" in req.body){
        for (const contact of contacts){
            const contactID = req.body.id;
            if (contactID === contact.id) {
                await data.deleteContact(contactID);
            }
        }
        res.send(contacts);
    }
})

// contactlog page
app.get("/admin/contactlog", authenticate, async (req, res)=>{
    const contacts = await data.getContacts();
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
app.get("/api/sale", async (req, res)=>{
    const result = await data.getRecentSales();
    res.send(result[0]);
})

app.post("/api/sale", authenticate, async (req, res)=>{
    const message = req.body.message;
    const result = await data.addSale(message);
    res.end(result);
})

app.delete("/api/sale", authenticate, async (req, res)=>{
    const result = await data.endSale();
    res.send(result);
})

app.get("/admin/salelog", authenticate, async (req, res) => {
    const result = await data.getRecentSales();
    res.send(result);
});


// 404 not found page
app.use((req, res) => {
    res.status(404).render("404.pug");
})

app.listen(port, ()=>{
    console.log(`Listening on port ${port}`)
});
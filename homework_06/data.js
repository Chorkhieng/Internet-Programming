// data file
// this package behaves just like the mysql one, but uses async await instead of callbacks.
const mysql = require(`mysql-await`); // npm install mysql-await
// first -- I want a connection pool: https://www.npmjs.com/package/mysql#pooling-connections
// this is used a bit differently, but I think it's just better -- especially if server is doing heavy work.
var connPool = mysql.createPool({
    connectionLimit: 5, // it's a shared resource, let's not go nuts.
    host: "127.0.0.1",// this will work
    user: "your username (same as database username",
    database: "your database username",
    password: "your database password", // we really shouldn't be saving this here long-term
    // -- and I probably shouldn't be sharing it with you...
});
// later you can use connPool.awaitQuery(query, data) -- it will return a promise
// for the query results.
async function addContact(data){
    // you CAN change the parameters for this function. please do not change the
    // parameters for any other function in this file.
    return await connPool.awaitQuery(`INSERT INTO contact (first, last, email, bookDate, translator, choice) VALUES (?, ?, ?, ?, ?, ?)`, 
                                            [data.first, data.last, data.email, data.bookDate,
                                            data.translator, data.choice]);
}
async function deleteContact(id){
    // get contact and delete by id
    const result = await connPool.awaitQuery(`DELETE FROM contact WHERE id = ?`, [id]);

    // return true/false to indicate succession
    if (result === null) {
        return false;
    }
    return true;
}
async function getContacts() {
    // get all contacts
    return await connPool.awaitQuery(`SELECT * FROM contact`);
}
async function addSale(message) {
    // add sale message to database   
    await connPool.awaitQuery('INSERT INTO sale (message, active, start_time) VALUES (?, ?, CURRENT_TIMESTAMP)', [message, true]);
}
async function endSale() {
    // end sale

    await connPool.awaitQuery(`UPDATE sale SET active = ?, end_time = CURRENT_TIMESTAMP WHERE active = ?`, [false, true]);
}
async function getRecentSales() {
    // get recent sales
    return await connPool.awaitQuery('SELECT message, active FROM sale ORDER BY start_time DESC LIMIT ?', [3]);
}

module.exports = {addContact, getContacts, deleteContact, addSale, endSale,
getRecentSales}

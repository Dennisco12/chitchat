class DBStorage {
  constructor(con) {
    this.con = con;
  }

  query(sql) {
    this.con.query(sql, function (err, result) {
      if (err) throw err;
      console.log("Result: " + result);
    });
  }
}

module.exports = DBStorage;

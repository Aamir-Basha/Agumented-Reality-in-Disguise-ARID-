const mariadb = require('mariadb');

const pool = mariadb.createPool({
  host: '194.164.48.22', 
  user: 'dennis',
  password: 'angw8wuga9g-ABS',
  database: 'dennis',
  connectionLimit: 10,
  port: 3306
});

async function connectToDatabase() {
  let connection;
  try {
    connection = await pool.getConnection();
    console.log('Connected to the MariaDB database!');

    const rows = await connection.query("SELECT * FROM test");

    rows.forEach(row => {
        console.log(row);
    });

  } catch (err) {
    console.error('Error connecting to the database:', err);
  } finally {
    if (connection) connection.end();
  }
}

connectToDatabase();
const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const { pool, initDb } = require('./database');
const { validateExpenseCreate } = require('./models');

const app = express();
app.use(cors());
app.use(express.json());

// Initialize database on startup
initDb().catch(console.error);

app.post('/api/expenses', async (req, res) => {
  try {
    const expense = validateExpenseCreate(req.body);
    const amountInPaise = Math.round(expense.amount * 100);
    const expenseId = uuidv4();
    const createdAt = new Date().toISOString();

    const client = await pool.connect();
    try {
      // Idempotency check
      if (expense.idempotency_key) {
        const existing = await client.query(
          'SELECT * FROM expenses WHERE idempotency_key = $1',
          [expense.idempotency_key]
        );
        if (existing.rows.length > 0) {
          const row = existing.rows[0];
          return res.status(200).json({
            id: row.id,
            amount: row.amount / 100,
            category: row.category,
            description: row.description,
            date: row.date,
            created_at: row.created_at
          });
        }
      }

      await client.query(
        `INSERT INTO expenses (id, amount, category, description, date, created_at, idempotency_key)
         VALUES ($1, $2, $3, $4, $5, $6, $7)`,
        [expenseId, amountInPaise, expense.category, expense.description, expense.date, createdAt, expense.idempotency_key]
      );

      res.status(201).json({
        id: expenseId,
        amount: expense.amount,
        category: expense.category,
        description: expense.description,
        date: expense.date,
        created_at: createdAt
      });
    } finally {
      client.release();
    }
  } catch (error) {
    console.error(error);
    res.status(400).json({ detail: error.message });
  }
});

app.get('/api/expenses', async (req, res) => {
  try {
    const { category, sort } = req.query;
    let query = 'SELECT * FROM expenses WHERE 1=1';
    const params = [];
    let paramIndex = 1;

    if (category) {
      query += ` AND LOWER(category) = LOWER($${paramIndex})`;
      params.push(category);
      paramIndex++;
    }

    if (sort === 'date_asc') {
      query += ' ORDER BY date ASC, created_at ASC';
    } else {
      query += ' ORDER BY date DESC, created_at DESC';
    }

    const client = await pool.connect();
    try {
      const result = await client.query(query, params);
      const expenses = result.rows.map(row => ({
        id: row.id,
        amount: row.amount / 100,
        category: row.category,
        description: row.description,
        date: row.date,
        created_at: row.created_at
      }));
      res.json(expenses);
    } finally {
      client.release();
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ detail: 'Database error' });
  }
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// For Vercel serverless
module.exports = app;

// For local development
if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
}
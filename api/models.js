function validateExpenseCreate(data) {
  const { amount, category, description, date, idempotency_key } = data;

  if (!amount || amount <= 0) {
    throw new Error('Amount must be positive');
  }

  if (!category || !category.trim()) {
    throw new Error('Category cannot be empty');
  }

  if (!description || !description.trim()) {
    throw new Error('Description cannot be empty');
  }

  if (!date || !date.trim()) {
    throw new Error('Date cannot be empty');
  }

  return {
    amount: parseFloat(amount),
    category: category.trim(),
    description: description.trim(),
    date: date.trim(),
    idempotency_key
  };
}

module.exports = { validateExpenseCreate };
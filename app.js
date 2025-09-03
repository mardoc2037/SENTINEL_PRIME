const express = require('express');
const app = express();
const port = 3000;

// Set up routes for AI engine
app.get('/api/query', (req, res) => {
    const query = req.query.q;
    // Call the AI engine with the query and return the response
    res.json({ message: 'Hello from the AI!' });
});

// Start the server
app.listen(port, () => {
    console.log(`Server started on port ${port}`);
});

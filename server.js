// server.js
const express = require('express');
const path = require('path');
const app = express();

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Example backend route
app.get('/api/data', (req, res) => {
  res.json({ message: 'Hello from the backend!' });
});

// Fallback to serve index.html for any other route (for single-page applications)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


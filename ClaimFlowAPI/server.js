const express = require('express');
const bodyParser = require('body-parser');
const logger = require('./middlewares/logger');
const claimsRoutes = require('./controllers/claimsController');
const premiumRoutes = require('./controllers/premiumController');
const policyRoutes = require('./controllers/policyController');

require("dotenv").config();
const app = express();

app.use(bodyParser.json());
app.use(logger);

app.use('/claims', claimsRoutes);
app.use('/premium', premiumRoutes);
app.use('/policy', policyRoutes);

app.use((req, res) => {
    res.status(404).json({ error: 'Endpoint not found' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

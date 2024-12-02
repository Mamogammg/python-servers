const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors()); // Enable CORS
app.use(express.json()); // Parse JSON payloads
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded payloads

// In-memory data storage
const emailsByApp = {};
const newApps = [
    { name: "chatier", type: "whatsapp", scale: "8" },
    { name: "gmail", type: "mail", scale: "8" },
    { name: "dummy", type: "dummy", scale: "8" },
    { name: "chati", url: "https://turbowarp.org/fullscreen?project_url=https://mamogammg.github.io/scratch-projects/Chati.sb3", type: "iframe", scale: "8" },
];

// Route to receive and store emails
app.post('/send_email', (req, res) => {
   const appName = req.headers['appname'];
    const emailFrom = req.headers['from'];
    const emailTo = req.headers['to'];
    const emailText = req.headers['text'];

    // Validar que todos los campos requeridos están presentes
    if (!appName || !emailFrom || !emailTo || !emailText) {
        return res.status(400).json({ error: "Missing required headers" });
    }

    // Almacenar el email
    const email = { from: emailFrom, to: emailTo, text: emailText };
    if (!emailsByApp[appName]) {
        emailsByApp[appName] = [];
    }
    emailsByApp[appName].push(email);

    res.status(200).json({ message: "Email successfully saved" });
});

// Route to retrieve user emails for a specific app
app.get('/get_user_emails/:appName', (req, res) => {
    const { appName } = req.params;
    const { user_id } = req.query;

    if (!user_id) {
        return res.status(400).json({ error: "user_id parameter is missing" });
    }

    // Retrieve emails for the app and filter by user_id
    const emails = emailsByApp[appName] || [];
    const userEmails = emails.filter(email => email.to === user_id);

    res.status(200).json({ emails: userEmails });
});

// Route to retrieve the list of available apps
app.get('/get_apps', (req, res) => {
    res.status(200).json({ apps: newApps });
});

// Route to get the app logo (file serving)
app.get('/get_app_logo/:appName', (req, res) => {
    const { appName } = req.params;

    // Define the logo file path
    const logoPath = path.join(__dirname, "apps", `${appName}.png`);

    // Check if the file exists
    if (fs.existsSync(logoPath)) {
        res.sendFile(logoPath);
    } else {
        res.status(404).json({ error: "Logo not found" });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://0.0.0.0:${PORT}`);
});

const fs = require("fs");

// Write to a file
fs.writeFileSync("notes.txt", "Welcome to Vibe Coding Bootcamp!\n");
// Read from a file
const data = fs.readFileSync("notes.txt", "utf8");
console.log("📖 File Content:\n", data);

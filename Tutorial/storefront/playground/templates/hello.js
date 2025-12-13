// Typing animation
const text = "Welcome to Our Platform 👋";
const typingElement = document.getElementById("typingText");
let index = 0;

function typeText() {
    if (index < text.length) {
        typingElement.textContent += text.charAt(index);
        index++;
        setTimeout(typeText, 70);
    }
}

typeText();

// Dark mode toggle
const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    themeToggle.textContent =
        document.body.classList.contains("dark") ? "☀️" : "🌙";
});

// Button functionality
document.getElementById("startBtn").addEventListener("click", () => {
    const btn = document.getElementById("startBtn");
    btn.textContent = "Loading...";
    btn.disabled = true;

    setTimeout(() => {
        alert("Redirecting to dashboard 🚀");
        // window.location.href = "dashboard.html";
    }, 1200);
});

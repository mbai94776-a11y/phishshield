const scanBtn = document.getElementById("scanBtn");
const result = document.getElementById("result");
const statusText = document.getElementById("statusText");
const riskText = document.getElementById("riskText");

scanBtn.addEventListener("click", () => {
  const url = document.getElementById("urlInput").value;

  if (!url) {
    alert("Please enter a URL");
    return;
  }

  result.classList.remove("hidden");

  // Fake academic-safe logic
  const risk = Math.floor(Math.random() * 60);

  if (risk > 40) {
    statusText.innerText = "⚠️ SUSPICIOUS";
    statusText.style.color = "red";
  } else {
    statusText.innerText = "✅ SAFE";
    statusText.style.color = "#00e0c6";
  }

  riskText.innerText = `Risk Score: ${risk}`;
});

// Accordion
document.querySelectorAll(".accordion-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const content = btn.nextElementSibling;
    content.style.display =
      content.style.display === "block" ? "none" : "block";
  });
});

// Theme toggle
document.getElementById("themeToggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

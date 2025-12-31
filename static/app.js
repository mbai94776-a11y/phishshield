const scanBtn = document.getElementById("scanBtn");
const resultBox = document.getElementById("result");

scanBtn.addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value.trim();
  if (!url) {
    alert("Please enter a URL");
    return;
  }

  resultBox.classList.add("hidden");

  const res = await fetch("/scan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });

  const data = await res.json();

  resultBox.innerHTML = `
    <h3>${data.verdict} (${data.score}/100)</h3>
    <p><strong>Why this link is flagged:</strong></p>
    <ul>
      ${data.reasons.map(r => `<li>${r}</li>`).join("")}
    </ul>
  `;

  resultBox.classList.remove("hidden");
});

const scanBtn = document.querySelector("button");
const input = document.querySelector("input");

scanBtn.addEventListener("click", () => {
    const url = input.value.trim();

    if (!url) {
        alert("Please enter a URL");
        return;
    }

    showLoading();
    setTimeout(() => fakeScan(url), 2000);
});

function showLoading() {
    const result = document.getElementById("result");
    result.innerHTML = `
        <div class="loader"></div>
        <p>Analyzing link safely...</p>
    `;
    result.classList.add("show");
}

function fakeScan(url) {
    const score = Math.floor(Math.random() * 100);
    let status = "SAFE";
    let color = "safe";

    if (score > 70) {
        status = "DANGEROUS";
        color = "danger";
    } else if (score > 40) {
        status = "CAUTION";
        color = "warn";
    }

    document.getElementById("result").innerHTML = `
        <div class="result-card ${color}">
            <h2>${status}</h2>
            <p>Risk Score: ${score}/100</p>
            <small>Checked redirects, domain age, SSL & patterns</small>
        </div>
    `;
}

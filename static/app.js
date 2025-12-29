let lastResult = null;

document.getElementById("scanBtn").addEventListener("click", async () => {
    const url = document.getElementById("urlInput").value;
    if (!url) return alert("Enter a URL");

    document.getElementById("result").innerHTML = "Scanning...";
    
    const res = await fetch("/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    });

    const data = await res.json();
    lastResult = data;

    document.getElementById("result").innerHTML = `
        <div class="card ${data.verdict.toLowerCase()}">
            <h3>${data.verdict}</h3>
            <p>Risk Score: ${data.score}</p>
            <button id="downloadBtn">Download Report</button>
        </div>
    `;

    document.getElementById("downloadBtn").onclick = downloadReport;
});

async function downloadReport() {
    if (!lastResult) return alert("No scan data");

    const res = await fetch("/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(lastResult)
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "phishshield_report.pdf";
    a.click();
}

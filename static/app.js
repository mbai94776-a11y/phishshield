const scanBtn = document.getElementById("scanBtn");
const input = document.getElementById("urlInput");
const result = document.getElementById("result");

scanBtn.onclick = async () => {
    const url = input.value.trim();
    if (!url) return alert("Enter URL");

    result.innerHTML = "<div class='loader'></div>";

    const res = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url})
    });

    const data = await res.json();

    result.innerHTML = `
      <div class="card ${data.label}">
        <h2>${data.label}</h2>
        <p>Risk Score: ${data.score}</p>
        <button onclick='download(${JSON.stringify(data)}, "${url}")'>
          Download Report
        </button>
      </div>
    `;
};

function download(data, url){
    fetch("/report", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({...data, url})
    })
    .then(res=>res.blob())
    .then(blob=>{
        const a=document.createElement("a");
        a.href=URL.createObjectURL(blob);
        a.download="phishshield_report.pdf";
        a.click();
    });
}

document.getElementById("themeToggle").onclick=()=>{
    document.body.classList.toggle("light");
};

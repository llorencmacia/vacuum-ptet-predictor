const form = document.getElementById("params-form");
let lastSimData = null; 

function showTab(tabName) {
    const tabs = ['info', 'plots', 'data', 'model'];
    
    tabs.forEach(t => {
        const content = document.getElementById(`${t}-content`);
        const btn = document.getElementById(`btn-${t}`);
        
        // Si l'element existeix, li posem o treiem la classe 'hidden'
        if (content) {
            if (t === tabName) {
                content.classList.remove('hidden');
            } else {
                content.classList.add('hidden');
            }
        }
        
        // Gestionem la classe 'active' del botó
        if (btn) {
            btn.classList.toggle('active', t === tabName);
        }
    });

    // Redibuixar gràfics de Plotly
    if (tabName === 'plots') {
        window.dispatchEvent(new Event('resize'));
    }
}

function generateTable(data) {
    lastSimData = data; 
    document.getElementById("btn-download").style.display = "inline-block";
    
    if (data.kpis) {
        document.getElementById("kpi-ref").innerText = data.kpis.ptet_ref.toFixed(2) + " s";
        document.getElementById("kpi-new").innerText = data.kpis.ptet_new.toFixed(2) + " s";
        const delta = data.kpis.delta_pct;
        const deltaElem = document.getElementById("kpi-delta");
        deltaElem.innerText = delta.toFixed(2) + " %";
        deltaElem.style.color = delta > 0 ? "#dc3545" : "#28a745";
        document.getElementById("kpi-error").innerText = data.kpis.max_abs_error.toFixed(2) + " s";
    }

    const ref = data.reference;
    const neu = data.new;
    let html = `<table><thead><tr><th>Pressure [bar]</th><th>Time Ref [s]</th><th>Time New [s]</th><th>Diff [s]</th></tr></thead><tbody>`;
    ref.x_time_table.forEach((p, i) => {
        const tRef = ref.t_table[i];
        const tNew = neu.t_table[i];
        const diff = tNew - tRef;
        html += `<tr><td>${(p / 1e5).toFixed(2)}</td><td>${tRef.toFixed(3)}</td><td>${tNew.toFixed(3)}</td><td style="color:${diff > 0 ? 'red' : 'green'}">${diff.toFixed(3)}</td></tr>`;
    });
    html += `</tbody></table>`;
    document.getElementById("tables-output").innerHTML = html;
}

form.addEventListener("submit", async function(e) {
    e.preventDefault();
    const btn = form.querySelector('button');
    btn.innerText = "Calculating...";
    btn.disabled = true;

    try {
        const response = await fetch("/plot", { method: "POST", body: new FormData(form) });
        const data = await response.json();

        // Actualitzar Gràfics
        const containers = {"pieceChart": data.piece_plot, "polyChart": data.poly_plot, "timeChart": data.time_plot, "errorChart": data.error_plot};
        for (const [id, html] of Object.entries(containers)) {
            const div = document.getElementById(id);
            div.innerHTML = html;
            div.querySelectorAll("script").forEach(oldScript => {
                const newScript = document.createElement("script");
                newScript.text = oldScript.text;
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        }
        // Actualitzar Taula i KPIs
        generateTable(data);
        generateModelTable(data);

    } catch (error) { console.error(error); }
    btn.innerText = "Update Plots";
    btn.disabled = false;
});

async function exportToCSV() {
    const response = await fetch("/download", {
        method: "POST",
        body: new FormData(document.getElementById("params-form"))
    });

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "simulation_full.csv";
    a.click();
}

function generateModelTable(data) {
    if (!data.model_data) {
        console.error("Dades del model no trobades en la resposta.");
        return;
    }

    const ref = data.model_data.reference;
    const neu = data.model_data.new;
    // També enviem conditions al JSON, oi? Les podem fer servir
    const cond = data.conditions; 

    const fmtExp = (val) => (val !== undefined && val !== null) ? val.toExponential(3) : "N/A";
    const fmtNum = (val, dec) => (val !== undefined && val !== null) ? val.toFixed(dec) : "N/A";

    let html = `
    <table>
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Reference</th>
                <th>New</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Coef. a</td><td>${fmtExp(ref.a)}</td><td>${fmtExp(neu.a)}</td></tr>
            <tr><td>Coef. b</td><td>${fmtExp(ref.b)}</td><td>${fmtExp(neu.b)}</td></tr>
            <tr><td>Coef. c</td><td>${fmtExp(ref.c)}</td><td>${fmtExp(neu.c)}</td></tr>
            <tr><td>Coef. d</td><td>${fmtExp(ref.d)}</td><td>${fmtExp(neu.d)}</td></tr>
            <tr>
                <td>p_min [bar]</td>
                <td>${fmtNum(ref.p_min / 1e5, 3)}</td>
                <td>${fmtNum(neu.p_min / 1e5, 3)}</td>
            </tr>
            <tr>
                <td>ṁ_max [kg/s]</td>
                <td>${fmtNum(ref.dotm_max, 4)}</td>
                <td>${fmtNum(neu.dotm_max, 4)}</td>
            </tr>
        </tbody>
    </table>`;
    
    document.getElementById("model-output").innerHTML = html;
}
// Quan la pàgina es carregui, ens assegurem que la pestanya info és l'única visible
document.addEventListener("DOMContentLoaded", () => {
    showTab('info');
});
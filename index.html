let token = null;
let tenant_id = null;

// Afficher formulaire inscription / login
document.getElementById("showRegister").onclick = () => {
    document.getElementById("loginFormDiv").style.display = "none";
    document.getElementById("registerFormDiv").style.display = "block";
};
document.getElementById("showLogin").onclick = () => {
    document.getElementById("loginFormDiv").style.display = "block";
    document.getElementById("registerFormDiv").style.display = "none";
};

// Inscription
document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const nom = document.getElementById("registerNom").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    const tId = parseInt(document.getElementById("registerTenant").value);

    const res = await fetch("http://127.0.0.1:5000/users/register", {
        method:"POST",
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({nom, email, password, tenant_id:tId})
    });
    const data = await res.json();
    if(data.status==="success") alert("Compte créé, connectez-vous !");
    else alert(data.message);
});

// Connexion
document.getElementById("loginForm").addEventListener("submit", async (e)=>{
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const res = await fetch("http://127.0.0.1:5000/users/login", {
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({email, password})
    });
    const data = await res.json();
    if(data.status==="success"){
        token = data.token;
        tenant_id = data.tenant_id;
        document.getElementById("userName").innerText = data.nom;
        document.getElementById("authSection").style.display="none";
        document.getElementById("dashboard").style.display="block";
        loadAll();
    } else alert(data.message);
});

// Déconnexion
document.getElementById("logoutBtn").onclick = ()=>{
    token = null;
    tenant_id = null;
    document.getElementById("dashboard").style.display="none";
    document.getElementById("authSection").style.display="block";
};

// Charger tous les modules
async function loadAll(){
    await loadProjects();
    await loadPipelines();
    await loadLogs();
    await loadBilling();
}

// --- Projets ---
async function loadProjects(){
    const res = await fetch(`http://127.0.0.1:5000/projects`, {
        headers:{'x-access-token': token}
    });
    const projects = await res.json();

    const table = document.getElementById("projectsTable");
    table.innerHTML = `<tr>
        <th>ID</th><th>Nom</th><th>Template</th><th>Date</th><th>Action</th>
    </tr>`;
    let counts = {Web:0, Mobile:0, API:0};

    projects.forEach(p=>{
        const row = table.insertRow();
        row.insertCell(0).innerText = p.project_id;
        row.insertCell(1).innerText = p.nom;
        row.insertCell(2).innerText = p.type_template;
        row.insertCell(3).innerText = p.date_creation;

        const btnCell = row.insertCell(4);
        const btn = document.createElement("button");
        btn.innerText="Supprimer";
        btn.className="deleteBtn";
        btn.onclick = async ()=>{ await fetch(`http://127.0.0.1:5000/projects/${p.project_id}`, {method:"DELETE", headers:{'x-access-token': token}}); loadProjects();};
        btnCell.appendChild(btn);

        counts[p.type_template]++;
    });

    // Graphique
    const ctx = document.getElementById("projectsChart").getContext("2d");
    new Chart(ctx, {
        type:'bar',
        data:{
            labels:['Web','Mobile','API'],
            datasets:[{
                label:'Projets',
                data:[counts.Web, counts.Mobile, counts.API],
                backgroundColor:['#4CAF50','#FF9800','#2196F3']
            }]
        },
        options:{responsive:true, plugins:{legend:{display:false}}}
    });
}

// --- Pipelines ---
async function loadPipelines(){
    const res = await fetch("http://127.0.0.1:5000/pipelines", {headers:{'x-access-token':token}});
    const pipelines = await res.json();
    const table = document.getElementById("pipelinesTable");
    table.innerHTML = `<tr>
        <th>ID</th><th>Projet</th><th>Status</th><th>Dernier Run</th>
    </tr>`;
    let statusCounts = {pending:0, success:0, failed:0};
    pipelines.forEach(p=>{
        const row = table.insertRow();
        row.insertCell(0).innerText = p.pipeline_id;
        row.insertCell(1).innerText = p.project_id;
        row.insertCell(2).innerText = p.status;
        row.insertCell(3).innerText = p.last_run || "-";
        statusCounts[p.status] = (statusCounts[p.status]||0)+1;
    });

    const ctx = document.getElementById("pipelinesChart").getContext("2d");
    new Chart(ctx, {
        type:'pie',
        data:{
            labels:['Pending','Success','Failed'],
            datasets:[{
                label:'Pipelines',
                data:[statusCounts.pending||0,statusCounts.success||0,statusCounts.failed||0],
                backgroundColor:['#f39c12','#2ecc71','#e74c3c']
            }]
        }
    });
}

// --- Logs ---
async function loadLogs(){
    const res = await fetch("http://127.0.0.1:5000/logs", {headers:{'x-access-token':token}});
    const logs = await res.json();
    const table = document.getElementById("logsTable");
    table.innerHTML = `<tr>
        <th>ID</th><th>Projet</th><th>Niveau</th><th>Message</th><th>Timestamp</th>
    </tr>`;
    logs.forEach(l=>{
        const row = table.insertRow();
        row.insertCell(0).innerText = l.log_id;
        row.insertCell(1).innerText = l.project_id;
        row.insertCell(2).innerText = l.niveau;
        row.insertCell(3).innerText = l.message;
        row.insertCell(4).innerText = l.timestamp;
    });
}

// --- Facturation ---
async function loadBilling(){
    const res = await fetch("http://127.0.0.1:5000/billing", {headers:{'x-access-token':token}});
    const bills = await res.json();
    const table = document.getElementById("billingTable");
    table.innerHTML = `<tr><th>ID</th><th>Montant</th><th>Date</th></tr>`;
    bills.forEach(b=>{
        const row = table.insertRow();
        row.insertCell(0).innerText = b.billing_id;
        row.insertCell(1).innerText = b.montant;
        row.insertCell(2).innerText = b.date_facturation;
    });
}

// --- Création projet ---
document.getElementById("projectForm").addEventListener("submit", async e=>{
    e.preventDefault();
    const nom = document.getElementById("projectName").value;
    const type_template = document.getElementById("projectType").value;
    await fetch("http://127.0.0.1:5000/projects", {
        method:"POST",
        headers:{'Content-Type':'application/json','x-access-token':token},
        body: JSON.stringify({nom, type_template})
    });
    document.getElementById("projectForm").reset();
    loadProjects();
});
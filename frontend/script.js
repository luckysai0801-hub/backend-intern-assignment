let token = "";

const API = "http://127.0.0.1:8000/api/v1";

function showMessage(msg) {
    document.getElementById("message").innerText = msg;
}

async function register() {
    const res = await fetch(`${API}/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: regName.value,
            email: regEmail.value,
            password: regPassword.value
        })
    });
    const data = await res.json();
    showMessage(data.message || data.detail);
}

async function login() {
    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: loginEmail.value,
            password: loginPassword.value
        })
    });
    const data = await res.json();
    token = data.access_token;
    showMessage("Login successful");
}

async function createTask() {
    const res = await fetch(`${API}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            title: taskTitle.value,
            description: taskDesc.value
        })
    });
    showMessage("Task created");
}

async function getTasks() {
    const res = await fetch(`${API}/tasks`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    });
    const tasks = await res.json();
    const list = document.getElementById("taskList");
    list.innerHTML = "";
    tasks.forEach(t => {
        const li = document.createElement("li");
        li.innerText = t.title;
        list.appendChild(li);
    });
}

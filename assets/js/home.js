const pb = new PocketBase('https://atendimento-fraterno.pockethost.io');

document.getElementById("buttonLogin").addEventListener("click", async function() {
    const login = document.getElementById("inputLogin");
    const password = document.getElementById("inputPassword");
    const loginForm = document.getElementById(`formLogin`);
    const passwordForm = document.getElementById(`formPassword`);

    if(!(checkLogin(login.value))){
        console.log("E-mail inválido!");
        loginForm.classList.add("error");
        loginForm.classList.remove("success");
        showErrorBubble("Login inválido! Exemplo: atendente1");
        return;
    }

    loginForm.classList.add("success");
    loginForm.classList.remove("error");

    if(!(checkPassword(password.value))){
        console.log("Senha inválida!");
        passwordForm.classList.add("error");
        passwordForm.classList.remove("success");
        showErrorBubble("Senha inválida!");
        return;
    }

    passwordForm.classList.add("success");
    passwordForm.classList.remove("error");

    const authData = await pb.collection('staff').authWithPassword(
        login.value,
        password.value,
    );

    console.log(authData);
    console.log(pb.authStore.isValid);
    console.log(pb.authStore.token);
    console.log(pb.authStore.model.id);
})

function checkLogin(login) {
    return login.includes("atendimentofraterno.saj");
}

function checkPassword(password) {
    let test = true;
    if(password.length < 8) test = false;
    return test;
}

async function hashSHA256(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
    return hashHex;
}

timer = 0;

function showErrorBubble(string) {
    const bubble = document.getElementById('errorBubble');

    bubble.style.left = `auto`;
    bubble.style.bottom = `90%`;
    bubble.innerHTML = `<h4><strong>Hey!</strong> ${string}</h4>`;
    bubble.style.display = 'block'

    setTimeout(() => {
        if(timer <= 0) hideErrorBubble()
    }, 1000 * 5)

    timer = 5;
}

function hideErrorBubble() {
    document.getElementById('errorBubble').style.display = 'none';
}

setInterval(() => {
    timer -= 1;
}, 1000)
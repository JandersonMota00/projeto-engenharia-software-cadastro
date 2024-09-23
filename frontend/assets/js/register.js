document.getElementById("login").addEventListener("click", async function() {
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const confirm = document.getElementById("confirm");
    const emailForm = document.getElementById(`formEmail`);
    const passwordForm = document.getElementById(`formPassword`);
    const confirmForm = document.getElementById(`formConfirm`);

    if(!(checkEmail(email.value))){
        console.log("E-mail inválido!");
        emailForm.classList.add("error");
        emailForm.classList.remove("success");
        showErrorBubble("E-mail inválido,  exemplo: exemplo@gmail.com");
        return;
    }

    emailForm.classList.add("success");
    emailForm.classList.remove("error");

    if(!(checkPassword(password.value))){
        console.log("Senha inválida!");
        passwordForm.classList.add("error");
        passwordForm.classList.remove("success");
        showErrorBubble("Senha inválida, experimente usar ao menos 8 caracteres.");
        return;
    }

    passwordForm.classList.add("success");
    passwordForm.classList.remove("error");

    if(!(checkConfirm(password.value, confirm.value))) {
        console.log("Senhas diferentes!");
        confirmForm.classList.add("error");
        confirmForm.classList.remove("success");
        showErrorBubble("Senha de confirmação inválida, as senhas devem ser iguais!");
        return;
    }

    confirmForm.classList.add("success");
    confirmForm.classList.remove("error");

    console.log("output: " + email.value + " " + await hashSHA256(password.value) + " " + await hashSHA256(confirm.value));
})

function checkEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
}

function checkConfirm(password, confirm){
    let test = true;
    if(password != confirm) test = false;
    return test;
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
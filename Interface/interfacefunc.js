const signUpButton = document.getElementById('signup');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click',() => {
    container.classList.add("right-planel-activate");
});

signInButton.addEventListener('click',() => {
    container.classList.remove("right-planel-activate");
});


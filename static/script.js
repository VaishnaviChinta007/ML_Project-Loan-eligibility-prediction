document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loanForm");
    if (form) {
        form.addEventListener("submit", () => {
            form.querySelector("button").innerText = "Checking...";
        });
    }
});

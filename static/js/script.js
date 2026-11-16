document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#prediction-form");
    if (!form) return;

    form.addEventListener("submit", (event) => {
        if (!form.reportValidity()) {
            event.preventDefault();
            return;
        }
        const button = form.querySelector("button[type='submit']");
        button.disabled = true;
        button.textContent = "Generating prediction...";
    });
});

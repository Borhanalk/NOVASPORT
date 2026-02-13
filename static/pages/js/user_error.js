document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const fields = form.querySelectorAll(".input-container");

    form.addEventListener("submit", function (e) {
        let hasError = false;

        fields.forEach((field) => {
            const input = field.querySelector("input");
            const errorMessage = field.querySelector(".error-message");

            if (input && !input.value.trim()) {
                e.preventDefault();
                hasError = true;
                field.classList.add("error");
                errorMessage.classList.add("visible");
            } else {
                field.classList.remove("error");
                errorMessage.classList.remove("visible");
            }
        });

        if (!hasError) {
            form.submit();
        }
    });
});

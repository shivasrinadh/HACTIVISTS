document.addEventListener("DOMContentLoaded", () => {
    const amountInput = document.querySelector('input[name="claim_amount"]');
    if (amountInput) {
        amountInput.addEventListener("blur", () => {
            const value = Number(amountInput.value);
            if (!Number.isNaN(value) && value > 0) {
                amountInput.value = value.toFixed(2);
            }
        });
    }

    const claimForm = document.querySelector("#claim-form");
    if (claimForm) {
        claimForm.addEventListener("submit", (event) => {
            const requiredFields = claimForm.querySelectorAll("[data-required='true']");
            let invalid = false;
            requiredFields.forEach((field) => {
                if (!field.value || !field.value.toString().trim()) {
                    invalid = true;
                    field.style.borderColor = "#b91c1c";
                } else {
                    field.style.borderColor = "";
                }
            });
            if (invalid) {
                event.preventDefault();
                alert("Please complete all required fields before submitting.");
            }
        });
    }
});

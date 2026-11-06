// Small client-side enhancement: prevent accidental empty amount submissions.
document.querySelectorAll(".transaction-form").forEach((form) => {
  form.addEventListener("submit", (event) => {
    const amount = Number(form.querySelector('[name="amount"]').value);
    if (!Number.isFinite(amount) || amount <= 0) {
      event.preventDefault();
      alert("Please enter an amount greater than zero.");
    }
  });
});

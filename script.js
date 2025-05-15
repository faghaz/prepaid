

document.getElementById('tokenForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const meter = document.getElementById('meter').value;
  const disco = document.getElementById('disco').value;
  const amount = document.getElementById('amount').value;

  if (meter && disco && amount >= 100) {
    // Simulated token purchase process
    document.getElementById('successMsg').style.display = 'block';
    console.log("Purchasing token for:", meter, disco, amount);

    // Reset the form
    this.reset();

    // Hide success message after a few seconds
    setTimeout(() => {
      document.getElementById('successMsg').style.display = 'none';
    }, 3000);
  }
});
// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const resultDiv = document.querySelector(".result");

    // Hide result initially
    if (resultDiv) {
        resultDiv.style.display = "none";
    }

    // Show result with fade-in when form is submitted
    form.addEventListener("submit", function() {
        if (resultDiv) {
            setTimeout(() => {
                resultDiv.style.display = "block";
                resultDiv.style.opacity = 0;
                let opacity = 0;
                const fadeIn = setInterval(() => {
                    opacity += 0.05;
                    resultDiv.style.opacity = opacity;
                    if (opacity >= 1) clearInterval(fadeIn);
                }, 20);
            }, 100); // small delay to wait for server response
        }
    });
});

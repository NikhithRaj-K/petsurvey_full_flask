// q2 checkbox disable js
 document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("other_q2_input");

    function updateOtherInputVisibility() {
        const isOthersChecked = document.querySelector('input[name="answer2"][value="Others"]').checked;
        input.style.display = isOthersChecked ? "inline" : "none";
        input.disabled = !isOthersChecked;
        if (!isOthersChecked) input.value = ""; // Optional: Clear input when hidden
    }

    document.querySelectorAll('input[name="answer2"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateOtherInputVisibility);
    });
});

// q4 radio disable js
 document.addEventListener("DOMContentLoaded", function () {
        const input = document.getElementById("other_q4_input");

        function toggleOtherInput(show) {
            input.style.display = show ? "inline" : "none";
            input.disabled = !show;
        }


        document.querySelectorAll('input[name="answer4"]').forEach(radio => {
            radio.addEventListener('click', () => {
                toggleOtherInput(radio.value === "Others");
            });
        });
    });

 // q5 checkbox disable js
 document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("other_q5_input");

    function updateOtherInputVisibility() {
        const isOthersChecked = document.querySelector('input[name="answer5"][value="Others"]').checked;
        input.style.display = isOthersChecked ? "inline" : "none";
        input.disabled = !isOthersChecked;
        if (!isOthersChecked) input.value = ""; // Optional: Clear input when hidden
    }

    document.querySelectorAll('input[name="answer5"]').forEach(checkbox => {
        checkbox.addEventListener('change', updateOtherInputVisibility);
    });
});

 // q6 radio disable js
 document.addEventListener("DOMContentLoaded", function () {
        const input = document.getElementById("other_q6_input");

        function toggleOtherInput(show) {
            input.style.display = show ? "inline" : "none";
            input.disabled = !show;
        }


        document.querySelectorAll('input[name="answer6"]').forEach(radio => {
            radio.addEventListener('click', () => {
                toggleOtherInput(radio.value === "Others");
            });
        });
    });

 // q7 radio disable js
 document.addEventListener("DOMContentLoaded", function () {
        const input = document.getElementById("other_q7_input");

        function toggleOtherInput(show) {
            input.style.display = show ? "inline" : "none";
            input.disabled = !show;
        }


        document.querySelectorAll('input[name="answer7"]').forEach(radio => {
            radio.addEventListener('click', () => {
                toggleOtherInput(radio.value === "Others");
            });
        });
    });

  // q11 radio disable js
 document.addEventListener("DOMContentLoaded", function () {
        const input = document.getElementById("other_q11_input");

        function toggleOtherInput(show) {
            input.style.display = show ? "inline" : "none";
            input.disabled = !show;
        }


        document.querySelectorAll('input[name="answer11"]').forEach(radio => {
            radio.addEventListener('click', () => {
                toggleOtherInput(radio.value === "Others");
            });
        });
    });

 // q2 checkbox validation
 // function validateCheckboxGroup() {
 //    const checkboxes2 = document.querySelectorAll('input[name="answer2"]');
 //    const checkboxes5 = document.querySelectorAll('input[name="answer5"]');
 //    const isChecked2 = Array.from(checkboxes2).some(cb => cb.checked);
 //    const isChecked5 = Array.from(checkboxes5).some(cb => cb.checked);
 //    if isChecked2 && isChecked5{
 //    document.getElementById("error").style.display = "none";
 //    }
 //    else { document.getElementById("error").style.display = "none";
 //    }
 //    return isChecked;
 //  }
 //
 //   // q5 checkbox validation
 // function validateCheckboxGroup() {
 //    const checkboxes5 = document.querySelectorAll('input[name="answer5"]');
 //    const isChecked = Array.from(checkboxes5).some(cb => cb.checked);
 //    document.getElementById("error").style.display = isChecked ? "none" : "block";
 //    return isChecked;
 //  }

// Mandatory validation for checkboxes
document.querySelector("form").addEventListener("submit", function(event) {
    const group1 = document.querySelectorAll('input[name="answer2"]');
    const group2 = document.querySelectorAll('input[name="answer5"]');
    const group3 = document.querySelectorAll('input[name="answer10"]');

    const group1Checked = Array.from(group1).some(cb => cb.checked);
    const group2Checked = Array.from(group2).some(cb => cb.checked);
    const group3Checked = Array.from(group3).some(cb => cb.checked);

    if (!group1Checked || !group2Checked || !group3Checked) {
        event.preventDefault(); // Stop form submission
        alert("Please select at least one option in each required checkbox group.");
    }
});

// Auto hide form submission alert flash after 3 seconds
  setTimeout(() => {
    const flashContainer = document.getElementById("flash-container");
    if (flashContainer) {
      flashContainer.style.transition = "opacity 0.5s ease-out";
      flashContainer.style.opacity = "0";
      setTimeout(() => flashContainer.remove(), 500);  // Remove from DOM after fade
    }
  }, 3000);
const progressSteps = document.querySelectorAll(".progress-step");
const progressBars = document.querySelectorAll(".progress-bar");
const previousButton = document.getElementById("previous-button");
const form = document.querySelector("form");

let currentStep = 1;

function showCurrentStep() {
  progressSteps.forEach((step, index) => {
    if (index < currentStep) {
      step.classList.add("active");
    } else {
      step.classList.remove("active");
    }
  });

  updateProgressBar();
}

function updateProgressBar() {
  const actives = document.querySelectorAll(".progress-step.active");
  const progressStepsCount = progressSteps.length;
  const progressBarWidth = (actives.length - 1) / (progressStepsCount - 1) * 100;

  progressBars.forEach((progressBar) => {
    progressBar.style.width = `${progressBarWidth}%`;
  });
}

function nextStep() {
  currentStep++;
  showCurrentStep();
}

function previousStep() {
  currentStep--;
  showCurrentStep();
}

previousButton.addEventListener("click", previousStep);

form.addEventListener("submit", (event) => {
  event.preventDefault();
  nextStep();
});

showCurrentStep();
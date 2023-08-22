const container = document.querySelector('.circular-container');
const input = document.querySelector('.circular-input');
const centerX = container.offsetWidth / 2;
const centerY = container.offsetHeight / 2;
const radius = container.offsetWidth / 2 - input.offsetWidth / 2;
let isDragging = false;

const output = document.querySelector('.circular-output');
outputValue = 0;
finalOutput = 0;

// Set the initial position of the input circle to the top of the container
input.style.left = centerX - input.offsetWidth / 2 + 'px';
input.style.top = centerY - radius -10 + 'px'; // Adjusted initial position

input.addEventListener('mousedown', (event) => {
  isDragging = true;
  input.style.cursor = 'grabbing';
});

document.addEventListener('mousemove', (event) => {
  if (!isDragging) return;

  const deltaX = event.clientX - centerX;
  const deltaY = centerY - event.clientY;

  if (finalOutput == 1 && deltaX <= 5) {
    return;
  }

  if (finalOutput == 100 && deltaX >= 0) {
    return;
    }

  let angle = Math.atan2(deltaY, deltaX);

  if (angle < 0) {
    angle = 2 * Math.PI + angle; // Adjust for negative angles
  }

  const x = centerX + radius * Math.cos(angle);
  const y = centerY - radius * Math.sin(angle);

  input.style.left = x - input.offsetWidth / 2 + 'px';
  input.style.top = y - input.offsetHeight / 2 + 'px';

  // Calculate the output value based on the input circle's position
  outputValue = Math.round((angle / (2 * Math.PI)) * 100) -25;
  
  finalOutput = 100 - (outputValue < 0 ? 100 + outputValue : outputValue);

  // Adjust the output value for the full circle loop
  output.textContent = finalOutput;
});

document.addEventListener('mouseup', () => {
  isDragging = false;
  input.style.cursor = 'grab';
});

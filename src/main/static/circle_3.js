function startCircle3Script() {

const container = document.querySelector('.extern-3');
const input = document.querySelector('.circular-input-3');
const RotatingCircle = document.getElementById('rotating-circle-3');
const output = document.querySelector('#circle-output-3');

const centerX = container.offsetWidth / 2;
const centerY = container.offsetHeight / 2;
const radius = container.offsetWidth / 2 - input.offsetWidth / 2 -5;
let isDragging = false;
const bodyElement = document.querySelector('body');


outputValue = 1;
finalOutput = 1;

// Set the initial position of the input circle to the top of the container
input.style.left = centerX - input.offsetWidth / 2 + 'px';
input.style.top = centerY - radius -11  + 'px'; // Adjusted initial position

RotatingCircle.setAttribute('stroke-dashoffset', 375);
RotatingCircle.style.stroke = "#384AEB"

input.addEventListener('mousedown', (event) => {
  isDragging = true;
  input.style.cursor = 'grabbing';
  bodyElement.style.userSelect = 'none';
});

const containerRect = container.getBoundingClientRect();
const containerX = containerRect.left + container.offsetWidth / 2;
const containerY = containerRect.top + container.offsetHeight / 2;
const containerWidth = container.offsetWidth;
const containerHeight = container.offsetHeight;

setInput();

function setInput() {
  let angle = 1.25
  // Calculate the circle's position based on the angle and radius
  const x = containerX + radius * Math.cos(angle);
  const y = containerY - radius * Math.sin(angle);

  // Adjust x and y for the input's position within the container
  const inputX = x - containerWidth / 2; // Subtract container's width
  const inputY = y - containerHeight / 2;

  input.style.left = inputX - input.offsetWidth / 2 - (containerRect.x - (containerWidth / 2))  + 'px';
  input.style.top = inputY - input.offsetHeight / 2 - (containerRect.y - (containerHeight / 2)) + 'px';

  // Calculate the output value based on the input circle's position
  outputValue = Math.round((angle / (2 * Math.PI)) * 100) -25;

  finalOutput = 100 - (outputValue < 0 ? 100 + outputValue : outputValue);

  // Adjust the output value for the full circle loop
  output.textContent = finalOutput;


  RotatingCircle.setAttribute('stroke-dashoffset', 375 - (finalOutput * 3.75));
}

document.addEventListener('mousemove', async (event) => {
  if (!isDragging) return;
  // Calculate the container's position on the page

  // Calculate the mouse position relative to the container's center
  const mouseX = event.clientX - containerX;
  const mouseY = containerY - event.clientY;

  if (finalOutput === 1 && mouseX <= 5) {
    return;
  }

  if (finalOutput > 99 && mouseX >= -5) {
    return;
    }

  // Calculate the angle based on the mouse position
  let angle = Math.atan2(mouseY, mouseX);

  if (angle < 0) {
    angle = 2 * Math.PI + angle; // Adjust for negative angles
  }

  // Calculate the circle's position based on the angle and radius
  const x = containerX + radius * Math.cos(angle);
  const y = containerY - radius * Math.sin(angle);

  // Adjust x and y for the input's position within the container
  const inputX = x - containerWidth / 2; // Subtract container's width
  const inputY = y - containerHeight / 2;

  input.style.left = inputX - input.offsetWidth / 2 - (containerRect.x - (containerWidth / 2))  + 'px';
  input.style.top = inputY - input.offsetHeight / 2 - (containerRect.y - (containerHeight / 2)) + 'px';

  // Calculate the output value based on the input circle's position
  outputValue = Math.round((angle / (2 * Math.PI)) * 100) -25;

  finalOutput = 100 - (outputValue < 0 ? 100 + outputValue : outputValue);

  // Adjust the output value for the full circle loop
  output.textContent = finalOutput;


  RotatingCircle.setAttribute('stroke-dashoffset', 375 - (finalOutput * 3.75));
  console.log(RotatingCircle.getAttribute('stroke-dashoffset'));

});

document.addEventListener('mouseup', () => {
  isDragging = false;
  bodyElement.style.userSelect = 'auto';
  input.style.cursor = 'grab';
});


function getRGB(ratio) {
  const fixedValues = [
    { ratio: 0, r: 255, g: 0, b: 0 },
    { ratio: 10, r: 255, g: 0, b: 0 },
    { ratio: 20, r: 255, g: 165, b: 0 },
    { ratio: 30, r: 0, g: 200, b: 0 },
    { ratio: 100, r: 0, g: 100, b: 0 }
  ];

  // Find the two fixed values between which the given ratio falls
  let lowerIndex = 0;
  let upperIndex = fixedValues.length - 1;

  for (let i = 0; i < fixedValues.length - 1; i++) {
    if (ratio >= fixedValues[i].ratio && ratio <= fixedValues[i + 1].ratio) {
      lowerIndex = i;
      upperIndex = i + 1;
      break;
    }
  }

  // Interpolate RGB values based on the ratio
  const lowerValue = fixedValues[lowerIndex];
  const upperValue = fixedValues[upperIndex];

  const ratioDiff = upperValue.ratio - lowerValue.ratio;
  const ratioOffset = ratio - lowerValue.ratio;

  const r = Math.round(
    lowerValue.r + (upperValue.r - lowerValue.r) * (ratioOffset / ratioDiff)
  );
  const g = Math.round(
    lowerValue.g + (upperValue.g - lowerValue.g) * (ratioOffset / ratioDiff)
  );
  const b = Math.round(
    lowerValue.b + (upperValue.b - lowerValue.b) * (ratioOffset / ratioDiff)
  );

  return `rgb(${r}, ${g}, ${b})`;
}

}

const initialSentence = [
  "Who are you?",
  "What your name?",
  "SOS",
  "I wanna eat sth",
  "I need water",
  "I need you",
  "Yes",
  "No"
];

const leftSection = document.querySelector(".section-left");
const rightSection = document.querySelector(".section-right");
const output = document.querySelector(".output");

const splitArray = (array) => {
  const mid = Math.ceil(array.length / 2);
  return [array.slice(0, mid), array.slice(mid)];
};

const renderSection = (section, array, handleClick) => {
  section.innerHTML = ""; 
  array.forEach((item) => {
    const p = document.createElement("p");
    p.textContent = item;
    p.style.cursor = "pointer"; 
    p.addEventListener("click", () => handleClick(item, array));
    section.appendChild(p);
  });
};

const initKeyboardUI = (array) => {
  const [leftArray, rightArray] = splitArray(array);

  renderSection(leftSection, leftArray, handleLeftClick);
  renderSection(rightSection, rightArray, handleRightClick);
};

const handleLeftClick = (selectedItem, array) => {
  if (array.length === 1) {
    output.value = selectedItem;
    initKeyboardUI(initialSentence);
    return;
  }
  
  const subArray = array.filter((item) => item !== selectedItem);
  const [newLeft, newRight] = splitArray([...subArray, selectedItem]);

  renderSection(leftSection, newLeft, handleLeftClick);
  renderSection(rightSection, newRight, handleRightClick);
};

const handleRightClick = (selectedItem, array) => {
  if (array.length === 1) {
    output.value = selectedItem;
    initKeyboardUI(initialSentence);
    return;
  }
  
  const subArray = array.filter((item) => item !== selectedItem);
  const [newLeft, newRight] = splitArray([...subArray, selectedItem]);

  renderSection(leftSection, newLeft, handleLeftClick);
  renderSection(rightSection, newRight, handleRightClick);
};

initKeyboardUI(initialSentence);


fetch('http://127.0.0.1:8888/predict', {
  method: 'GET',
  headers: {
      'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
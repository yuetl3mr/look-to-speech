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

let previousChoice = null;
let sameChoiceCount = 0;
let reset = true;
const splitArray = (array) => {
  const mid = Math.ceil(array.length / 2);
  return [array.slice(0, mid), array.slice(mid)];
};

const renderSection = (section, array) => {
  section.innerHTML = "";
  array.forEach((item) => {
    const p = document.createElement("p");
    p.textContent = item;
    section.appendChild(p);
  });
};

const initKeyboardUI = (array) => {
  const [leftArray, rightArray] = splitArray(array);

  renderSection(leftSection, leftArray);
  renderSection(rightSection, rightArray);

  handleAPIResponse(leftArray, rightArray);
};

const handleAPIResponse = (leftArray, rightArray) => {
  setTimeout(() => {
    fetch('http://127.0.0.1:8888/predict', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        const choice = data.choice;
        console.log(choice);

        if (choice === previousChoice) {
          sameChoiceCount++;
        } else {
          sameChoiceCount = 1;
          previousChoice = choice;
        }

        if (sameChoiceCount >= 2) {
          if (choice === -1 || choice === 0) {
            reset = true;
            handleAPIResponse(leftArray, rightArray);
            return;
          }
          if (reset === true) {
            reset = false;
            setTimeout(() => {
              if (choice === 1 && leftArray.length === 1) {
                output.value = leftArray[0];
                initKeyboardUI(initialSentence);
              } else if (choice === 2 && rightArray.length === 1) {
                output.value = rightArray[0];
                initKeyboardUI(initialSentence);
              } else {
                const selectedArray = choice === 1 ? leftArray : (choice === 2 ? rightArray : null);
                const [newLeft, newRight] = splitArray(selectedArray);

                renderSection(leftSection, newLeft);
                renderSection(rightSection, newRight);

                handleAPIResponse(newLeft, newRight);
              }
            });
          } else {
            handleAPIResponse(leftArray, rightArray);
          }
        } else {
          handleAPIResponse(leftArray, rightArray);
          return;
        }
      })
      .catch(error => console.error('Error:', error));
  }, 500);
};


initKeyboardUI(initialSentence);

const initialSentence = [
  "Who are you?",
  "What your name?",
  "SOS",
  "I wanna eat sth",
  "I need water",
  "I need you",
  "Yes",
  "No",
];

const leftSection = document.querySelector(".section-left");
const rightSection = document.querySelector(".section-right");
const output = document.querySelector(".output");

let previousChoice = null;
let sameChoiceCount = 0;
let reset = true;
let isFetching = false;

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
};

const speakText = (text) => {
  const utterance = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(utterance);
};

const handleAPIResponse = (leftArray, rightArray) => {
  if (!isFetching) return;

  setTimeout(() => {
    fetch("http://127.0.0.1:8888/predict", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const choice = data.choice;
        console.log(choice);

        const keyboard = document.querySelector(".keyboard");
        if (choice === -1) {
          keyboard.style.border = "3px solid rgba(255, 0, 0, 0.5)";
        } else {
          keyboard.style.border = "3px solid rgb(105, 223, 242)";
        }

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
                speakText(leftArray[0]); // Speak the selected text
                isFetching = false;
                initKeyboardUI(initialSentence);
              } else if (choice === 2 && rightArray.length === 1) {
                output.value = rightArray[0];
                speakText(rightArray[0]); // Speak the selected text
                isFetching = false;
                initKeyboardUI(initialSentence);
              } else {
                const selectedArray =
                  choice === 1 ? leftArray : choice === 2 ? rightArray : null;
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
      .catch((error) => console.error("Error:", error));
  }, 500);
};

document.getElementById("start").addEventListener("click", () => {
  if (isFetching) return;
  isFetching = true;
  initKeyboardUI(initialSentence);
  const [leftArray, rightArray] = splitArray(initialSentence);
  handleAPIResponse(leftArray, rightArray);
});

initKeyboardUI(initialSentence);

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("magic-form");
  const resultBlock = document.getElementById("result");
  const codeOutput = document.getElementById("code-output");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const intent = document.getElementById("intent").value.trim();
    const identity = document.getElementById("identity").value.trim();

    if (!intent || !identity) {
      alert("Заполни оба поля, пожалуйста.");
      return;
    }

    const fullText = `${intent} ${identity}`;
    const code = generateMagicCode(fullText);

    codeOutput.textContent = code;
    resultBlock.classList.remove("hidden");
  });

  function generateMagicCode(text) {
  const alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ";
  const clean = text.toUpperCase().replace(/[^А-Я0-9]/g, "");

  let numericString = "";
  for (let char of clean) {
    if (/[0-9]/.test(char)) {
      numericString += char;
    } else {
      const index = alphabet.indexOf(char);
      if (index !== -1) {
        numericString += (index + 1).toString();
      }
    }
  }

  // Сжимаем число до трехзначного
  let sum = numericString.split("").reduce((a, b) => a + Number(b), 0);

  while (sum > 999) {
    sum = sum.toString().split("").reduce((a, b) => a + Number(b), 0);
  }

  return sum.toString();
}

});

async function analyzeAnswer() {
  const question = document.getElementById("question").value.trim();
  const answer = document.getElementById("answer").value.trim();
  const total_marks = parseInt(document.getElementById("marks").value);

  if (!question || !answer || !total_marks) {
    alert("Please fill all fields.");
    return;
  }

  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("result").classList.add("hidden");

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, answer, total_marks })
    });

    const data = await response.json();

    document.getElementById("studentAnswer").textContent = answer;
    document.getElementById("score").textContent = `${data.score} / ${total_marks}`;
    document.getElementById("confidence").textContent = data.confidence_level;

    const mistakesUl = document.getElementById("mistakes");
    mistakesUl.innerHTML = "";
    data.mistakes.forEach(m => {
      const li = document.createElement("li");
      li.textContent = m;
      mistakesUl.appendChild(li);
    });

    document.getElementById("explanation").textContent = data.explanation;
    document.getElementById("improve").textContent = data.how_to_improve;

    const correctUl = document.getElementById("correctAnswer");
    correctUl.innerHTML = "";
    data.correct_answer.forEach(c => {
      const li = document.createElement("li");
      li.textContent = c;
      correctUl.appendChild(li);
    });

    document.getElementById("result").classList.remove("hidden");

  } catch (err) {
    alert("Error connecting to backend.");
    console.error(err);
  }

  document.getElementById("loading").classList.add("hidden");
}

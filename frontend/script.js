let currentQuestion = "";
let currentIndex = 0;
let totalQuestions = 0;
let score = 0;
const BASE_URL = "http://127.0.0.1:5000";

function startInterview() {
  const domain = document.getElementById("domain").value;
  const type = document.getElementById("type").value;
  const difficulty = document.getElementById("difficulty").value;
  totalQuestions = parseInt(document.getElementById("questionCount").value);
  currentIndex = 0;
  score = 0;
  nextQuestion(domain, type, difficulty);
}

function nextQuestion(domain, type, difficulty) {
  if (currentIndex >= totalQuestions) {
    showFinalScore();
    return;
  }

  fetch(`${BASE_URL}/generate_question`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ domain, interview_type: type, difficulty })
  })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      return res.json();
    })
    .then(data => {
      if (data.error || data.question.includes("Error")) {
        document.getElementById("question").innerText = "Failed to load question.";
        console.error("Backend error:", data.error || data.question);
        return;
      }
      currentQuestion = data.question;
      document.getElementById("question").innerText = `Q${currentIndex + 1}: ${currentQuestion}`;
      document.getElementById("modelAnswer").innerText = "";
      document.getElementById("userAnswer").innerText = "";
      document.getElementById("questionSection").style.display = "block";
    })
    .catch(error => {
      console.error("Fetch error:", error);
      document.getElementById("question").innerText = "Error fetching question.";
    });
}

function viewAnswer() {
  fetch(`${BASE_URL}/get_answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: currentQuestion })
  })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      return res.json();
    })
    .then(data => {
      if (data.error) {
        console.error("Backend error:", data.error);
        return;
      }
      document.getElementById("modelAnswer").innerText = `Answer: ${data.answer}`;
    })
    .catch(error => console.error("Fetch error:", error));
}

function record() {
  const userAnswer = document.getElementById("userAnswer");
  userAnswer.innerHTML = "🎙️ Listening... Please speak your answer...";

  fetch(`${BASE_URL}/transcribe`, { method: "POST" })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
      return res.json();
    })
    .then(data => {
      if (data.error) {
        userAnswer.innerHTML = "Error transcribing answer.";
        console.error("Backend error:", data.error);
        return;
      }
      const transcript = data.transcription;
      userAnswer.innerHTML = `🗣️ You said: ${transcript}`;

      // Evaluate answer
      fetch(`${BASE_URL}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: currentQuestion, answer: transcript })
      })
        .then(res => {
          if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
          return res.json();
        })
        .then(result => {
          if (result.error) {
            userAnswer.innerHTML += `<br>❌ Error evaluating answer.`;
            console.error("Backend error:", result.error);
            return;
          }
          const feedback = result.feedback;
          userAnswer.innerHTML += `<br>✅ Feedback: ${feedback}`;

          // Parse score from feedback
          const scoreMatch = feedback.match(/Score: ([\d.]+)/i);
          const answerScore = scoreMatch ? parseFloat(scoreMatch[1]) : 0;
          if (answerScore >= 0.8) score++; // Count as correct if score >= 0.8

          // Show Next Button
          const nextBtn = document.createElement("button");
          nextBtn.innerText = "➡️ Next Question";
          nextBtn.onclick = () => {
            currentIndex++;
            nextBtn.remove();
            const domain = document.getElementById("domain").value;
            const type = document.getElementById("type").value;
            const difficulty = document.getElementById("difficulty").value;
            nextQuestion(domain, type, difficulty);
          };
          document.getElementById("questionSection").appendChild(nextBtn);
        })
        .catch(error => {
          userAnswer.innerHTML += `<br>❌ Error evaluating answer.`;
          console.error("Fetch error:", error);
        });
    })
    .catch(error => {
      userAnswer.innerHTML = "Error transcribing answer.";
      console.error("Fetch error:", error);
    });
}

function listenQuestion() {
  fetch(`${BASE_URL}/speak`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: currentQuestion })
  })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      return response.blob();
    })
    .then(blob => {
      const audioURL = URL.createObjectURL(blob);
      const audio = new Audio(audioURL);
      audio.play();
    })
    .catch(error => console.error("Fetch error:", error));
}

function showFinalScore() {
  document.getElementById("question").innerText = "✅ Interview Completed!";
  document.getElementById("modelAnswer").innerText = "";
  document.getElementById("userAnswer").innerText = `Final Score: ${score} out of ${totalQuestions}`;
}

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true, audio: false })
  .then(stream => {
    const video = document.getElementById("video");
    video.srcObject = stream;
  })
  .catch(err => console.error("Webcam access denied", err));

setInterval(capturePose, 1000);

function capturePose() {
  const video = document.getElementById("video");
  if (!video || video.readyState !== 4) return;

  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);

  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append("image", blob, "snapshot.jpg");

    fetch(`${BASE_URL}/analyze_pose`, {
      method: "POST",
      body: formData
    })
      .then(res => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then(data => {
        document.getElementById("poseResult").innerText = data.result;
      })
      .catch(error => console.error("Fetch error:", error));
  }, "image/jpeg");
}
function summarizeVideo() {
  const link = document.getElementById("youtubeLink").value;
  const resultBox = document.getElementById("resultBox");

  if (!link.includes("youtube.com") && !link.includes("youtu.be")) {
    resultBox.textContent = "❌ Please enter a valid YouTube link.";
    return;
  }

  // Mock summary response – replace this with actual API call
  resultBox.textContent = "⏳ Summarizing video, please wait...";

  // Simulate loading
  setTimeout(() => {
    resultBox.textContent = "✅ Video Summary:\n\nThis is a placeholder summary for the video.\n(Replace this with your backend response)";
  }, 2000);
}

function comingSoon() {
  alert("This feature is coming soon! Stay tuned.");
}

async function summarizeVideo() {
  const link = document.getElementById("youtubeLink").value.trim();
  const resultBox = document.getElementById("resultBox");

  if (!link.includes("youtube.com") && !link.includes("youtu.be")) {
    resultBox.textContent = "❌ Please enter a valid YouTube link.";
    return;
  }

  resultBox.textContent = "⏳ Summarizing video, please wait...";

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: link })
    });

    const data = await response.json();

    if (response.ok) {
      resultBox.textContent = "✅ Summary:\n\n" + data.summary;
    } else {
      resultBox.textContent = "❌ Error: " + (data.error || "Unknown error.");
    }
  } catch (err) {
    resultBox.textContent = "❌ Failed to fetch summary.";
    console.error(err);
  }
}


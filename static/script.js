document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("subreddit-form");
  const input = document.getElementById("subreddit");
  const loading = document.getElementById("loading");
  const sentimentChart = document
    .getElementById("sentimentChart")
    .getContext("2d");
  const summaryText = document.getElementById("summary-text");
  const wordcloudImage = document.getElementById("wordcloud");
  const suggestionsBox = document.createElement("div");
  suggestionsBox.id = "suggestions-box";
  suggestionsBox.style.border = "1px solid #ccc";
  suggestionsBox.style.position = "absolute";
  suggestionsBox.style.backgroundColor = "white";
  suggestionsBox.style.zIndex = "1000";
  suggestionsBox.style.width = input.offsetWidth + "px";
  suggestionsBox.style.maxHeight = "150px";
  suggestionsBox.style.overflowY = "auto";

  input.parentNode.appendChild(suggestionsBox);

  input.addEventListener("input", async function () {
    const query = input.value.trim();
    suggestionsBox.innerHTML = "";
    if (!query) return;

    try {
      const response = await fetch(`/suggest_subreddits?q=${query}`);
      const subs = await response.json();

      subs.forEach((sub) => {
        const div = document.createElement("div");
        div.textContent = `r/${sub}`;
        div.style.padding = "5px";
        div.style.cursor = "pointer";
        div.addEventListener("click", () => {
          input.value = sub;
          suggestionsBox.innerHTML = "";
        });
        suggestionsBox.appendChild(div);
      });
    } catch (err) {
      console.error(err);
    }
  });

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const subreddit = input.value.trim();
    if (!subreddit) return;

    loading.style.display = "block";

    try {
      const response = await fetch(`/analyze/${subreddit}`);
      const data = await response.json();

      loading.style.display = "none";

      if (window.sentimentPie) {
        window.sentimentPie.destroy();
      }

      window.sentimentPie = new Chart(sentimentChart, {
        type: "pie",
        data: {
          labels: ["Positive", "Neutral", "Negative"],
          datasets: [
            {
              data: [
                data.sentiments.positive,
                data.sentiments.neutral,
                data.sentiments.negative,
              ],
              backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
            },
          ],
        },
        options: {
          responsive: true,
        },
      });

      wordcloudImage.src = `/wordcloud/${subreddit}.png`;
      summaryText.textContent = data.summary;
    } catch (err) {
      loading.style.display = "none";
      summaryText.textContent = "An error occurred. Please try again.";
      console.error(err);
    }
  });
});

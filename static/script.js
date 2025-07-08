document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("subreddit-form");
  const input = document.getElementById("subreddit");
  const loading = document.getElementById("loading");
  const sentimentChart = document
    .getElementById("sentimentChart")
    .getContext("2d");
  const summaryText = document.getElementById("summary-text");
  const navLinks = document.querySelectorAll(".nav-link");
  const sections = document.querySelectorAll(".section");

  // Navigation functionality
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetSection = this.getAttribute("data-section");

      // Remove active class from all links and sections
      navLinks.forEach((l) => l.classList.remove("active"));
      sections.forEach((s) => s.classList.remove("active"));

      // Add active class to clicked link and target section
      this.classList.add("active");
      document
        .getElementById(targetSection + "-section")
        .classList.add("active");
    });
  });

  // Subreddit suggestions
  const suggestionsBox = document.createElement("div");
  suggestionsBox.id = "suggestions-box";
  suggestionsBox.style.display = "none";

  const inputGroup = input.closest(".input-group");
  inputGroup.parentNode.insertBefore(suggestionsBox, inputGroup.nextSibling);

  input.addEventListener("input", async function () {
    const query = input.value.trim();
    suggestionsBox.innerHTML = "";

    if (!query) {
      suggestionsBox.style.display = "none";
      return;
    }

    try {
      const response = await fetch(`/suggest_subreddits?q=${query}`);
      const subs = await response.json();

      if (subs.length > 0) {
        suggestionsBox.style.display = "block";
        suggestionsBox.style.width = inputGroup.offsetWidth + "px";

        subs.forEach((sub) => {
          const div = document.createElement("div");
          div.textContent = `r/${sub}`;
          div.addEventListener("click", () => {
            input.value = sub;
            suggestionsBox.style.display = "none";
          });
          suggestionsBox.appendChild(div);
        });
      } else {
        suggestionsBox.style.display = "none";
      }
    } catch (err) {
      console.error("Error fetching suggestions:", err);
      suggestionsBox.style.display = "none";
    }
  });

  // Hide suggestions when clicking outside
  document.addEventListener("click", function (e) {
    if (!inputGroup.contains(e.target) && !suggestionsBox.contains(e.target)) {
      suggestionsBox.style.display = "none";
    }
  });

  // Trending subreddit analyze buttons
  document.querySelectorAll(".analyze-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const subreddit = this.getAttribute("data-subreddit");
      input.value = subreddit;

      // Switch to analyzer section
      navLinks.forEach((l) => l.classList.remove("active"));
      sections.forEach((s) => s.classList.remove("active"));
      document
        .querySelector('[data-section="analyzer"]')
        .classList.add("active");
      document.getElementById("analyzer-section").classList.add("active");

      // Trigger analysis
      analyzeSubreddit(subreddit);
    });
  });

  // Main form submission
  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const subreddit = input.value.trim();
    if (!subreddit) return;

    analyzeSubreddit(subreddit);
  });

  // Main analysis function
  async function analyzeSubreddit(subreddit) {
    loading.style.display = "block";
    suggestionsBox.style.display = "none";

    // Scroll to results
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });

    try {
      const response = await fetch(`/analyze/${subreddit}`);
      const data = await response.json();

      loading.style.display = "none";

      // Update stats
      updateStats(data);

      // Update sentiment chart
      updateSentimentChart(data.sentiments);

      // Update keywords
      updateKeywords(data.trending_keywords);

      // Update sample posts
      updateSamplePosts(data.sample_posts);

      // Update summary
      summaryText.textContent = data.summary;

      // Show results
      document.getElementById("results").style.display = "block";
      document.getElementById("ai-summary").style.display = "block";
    } catch (err) {
      loading.style.display = "none";
      summaryText.textContent =
        "An error occurred while analyzing the subreddit. Please try again.";
      console.error("Analysis error:", err);
    }
  }

  // Update statistics cards
  function updateStats(data) {
    document.getElementById("total-posts").textContent =
      data.total_posts.toLocaleString();
    document.getElementById("active-users").textContent =
      data.active_users.toLocaleString();
    document.getElementById("last-updated").textContent = new Date(
      data.last_updated
    ).toLocaleTimeString();
  }

  // Update sentiment chart
  function updateSentimentChart(sentiments) {
    if (window.sentimentPie) {
      window.sentimentPie.destroy();
    }

    window.sentimentPie = new Chart(sentimentChart, {
      type: "doughnut",
      data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [
          {
            data: [
              sentiments.positive,
              sentiments.neutral,
              sentiments.negative,
            ],
            backgroundColor: ["#4CAF50", "#FFC107", "#F44336"],
            borderWidth: 0,
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              padding: 20,
              font: {
                size: 12,
              },
            },
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        },
      },
    });
  }

  // Update trending keywords
  function updateKeywords(keywords) {
    const container = document.getElementById("keywords-container");
    container.innerHTML = "";

    keywords.forEach((keyword) => {
      const tag = document.createElement("div");
      tag.className = "keyword-tag";
      tag.textContent = keyword;
      container.appendChild(tag);
    });
  }

  // Update sample posts
  function updateSamplePosts(posts) {
    const container = document.getElementById("sample-posts");
    container.innerHTML = "";

    posts.forEach((post) => {
      const postCard = document.createElement("div");
      postCard.className = "post-card";

      postCard.innerHTML = `
        <div class="post-header">
          <div class="post-title">${post.title}</div>
          <span class="post-sentiment ${post.sentiment}">${post.sentiment}</span>
        </div>
        <div class="post-stats">
          <span><i class="fas fa-arrow-up"></i> ${post.score}</span>
          <span><i class="fas fa-comments"></i> ${post.comments}</span>
          <span><i class="fas fa-clock"></i> ${post.timestamp}</span>
        </div>
      `;

      container.appendChild(postCard);
    });
  }

  // Initialize chart canvas sizing
  const chartCanvas = document.getElementById("sentimentChart");
  chartCanvas.style.height = "300px";

  // Add smooth scrolling for internal links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Add loading animation to analyze buttons
  document.querySelectorAll(".analyze-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const originalText = this.innerHTML;
      this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
      this.disabled = true;

      setTimeout(() => {
        this.innerHTML = originalText;
        this.disabled = false;
      }, 2000);
    });
  });

  // Add intersection observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -100px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe elements for animation
  document
    .querySelectorAll(
      ".stat-card, .chart-section, .feature-card, .trending-card"
    )
    .forEach((el) => {
      el.style.opacity = "0";
      el.style.transform = "translateY(20px)";
      el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
      observer.observe(el);
    });

  // Add keyboard navigation
  document.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target === input) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }

    if (e.key === "Escape") {
      suggestionsBox.style.display = "none";
    }
  });

  // Add responsive handling for mobile
  function handleResize() {
    if (window.innerWidth <= 768) {
      suggestionsBox.style.width = "100%";
    } else {
      suggestionsBox.style.width = inputGroup.offsetWidth + "px";
    }
  }

  window.addEventListener("resize", handleResize);
  handleResize(); // Initial call
});

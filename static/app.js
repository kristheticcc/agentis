const form = document.querySelector("#trial-form");
const messageInput = document.querySelector("#patient-message");
const submitButton = form.querySelector("button");
const status = document.querySelector("#status");
const results = document.querySelector("#results");

function element(tag, text, className) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}

function renderResults(trials) {
  results.replaceChildren();
  if (!trials.length) {
    results.append(element("p", "No matching trials were returned."));
    return;
  }

  for (const trial of trials) {
    const card = document.createElement("article");
    card.className = "trial";
    const title = element("h2", trial.title || "Untitled trial");
    const meta = document.createElement("div");
    meta.className = "meta";
    meta.append(element("span", `Rank #${trial.rank}`, "rank"));
    const nctLink = document.createElement("a");
    nctLink.href = `https://clinicaltrials.gov/study/${encodeURIComponent(trial.nct_id)}`;
    nctLink.target = "_blank";
    nctLink.rel = "noopener noreferrer";
    nctLink.textContent = trial.nct_id;
    meta.append(nctLink);
    card.append(title, meta);
    if (trial.study_info) card.append(element("p", trial.study_info));
    if (trial.ranking_reasoning) card.append(element("p", trial.ranking_reasoning, "reason"));
    if (trial.contacts_and_locations) card.append(element("p", trial.contacts_and_locations, "reason"));
    results.append(card);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  submitButton.disabled = true;
  status.textContent = "Searching and ranking trials…";
  results.replaceChildren();

  try {
    const response = await fetch("/api/match-trials", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) {
      const detail = await response.json().catch(() => ({}));
      throw new Error(detail.detail || `Request failed (${response.status})`);
    }
    const output = await response.json();
    renderResults(output.results || []);
    status.textContent = `Found ${output.results?.length || 0} ranked trial result(s).`;
  } catch (error) {
    status.textContent = `Unable to find trials: ${error.message}`;
  } finally {
    submitButton.disabled = false;
  }
});

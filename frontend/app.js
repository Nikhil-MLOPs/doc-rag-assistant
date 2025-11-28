// Simple frontend for Doc RAG Assistant
// Uses same-origin API base so it works on localhost and EC2
const API_BASE = "";

// We wait for DOMContentLoaded so elements are ready
document.addEventListener("DOMContentLoaded", () => {
  const uploadForm = document.getElementById("upload-form");
  const fileInput = document.getElementById("file-input");
  const uploadStatus = document.getElementById("upload-status");

  const docsList = document.getElementById("documents-list");
  const refreshDocsBtn = document.getElementById("refresh-docs-btn");

  const qaForm = document.getElementById("qa-form");
  const questionInput = document.getElementById("question-input");
  const answerText = document.getElementById("answer-text");
  const sourcesList = document.getElementById("sources-list");
  const qaStatus = document.getElementById("qa-status");

  // ---- Upload document ----
  uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    uploadStatus.textContent = "";
    uploadStatus.className = "status";

    const file = fileInput.files[0];
    if (!file) {
      uploadStatus.textContent = "Please choose a file first.";
      uploadStatus.classList.add("error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      uploadStatus.textContent = "Uploading...";
      console.log("Uploading to:", `${API_BASE}/api/documents`);

      const response = await fetch(`${API_BASE}/api/documents`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Upload failed");
      }

      const data = await response.json();
      uploadStatus.textContent = `Uploaded: ${data.original_filename} (id: ${data.id})`;
      uploadStatus.classList.add("success");

      fileInput.value = "";
      await fetchDocuments();
    } catch (error) {
      console.error("Upload error:", error);
      uploadStatus.textContent = error.message || "Upload failed";
      uploadStatus.classList.add("error");
    }
  });

  // ---- Fetch documents ----
  async function fetchDocuments() {
    docsList.innerHTML = "";
    try {
      console.log("Fetching docs from:", `${API_BASE}/api/documents`);
      const response = await fetch(`${API_BASE}/api/documents`);
      if (!response.ok) {
        throw new Error("Failed to fetch documents");
      }
      const docs = await response.json();
      if (docs.length === 0) {
        docsList.innerHTML = "<li>No documents uploaded yet.</li>";
        return;
      }
      docs.forEach((doc) => {
        const li = document.createElement("li");
        li.textContent = `${doc.original_filename} (id: ${doc.id}, size: ${doc.size_bytes} bytes)`;
        docsList.appendChild(li);
      });
    } catch (error) {
      console.error("Fetch docs error:", error);
      docsList.innerHTML = "<li>Error loading documents.</li>";
    }
  }

  refreshDocsBtn.addEventListener("click", () => {
    fetchDocuments();
  });

  // ---- Ask question (RAG QA) ----
  qaForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    qaStatus.textContent = "";
    qaStatus.className = "status";
    answerText.textContent = "";
    sourcesList.innerHTML = "";

    const question = questionInput.value.trim();
    if (!question) {
      qaStatus.textContent = "Please enter a question.";
      qaStatus.classList.add("error");
      return;
    }

    try {
      qaStatus.textContent = "Thinking...";
      console.log("QA calling:", `${API_BASE}/api/qa`);

      const response = await fetch(`${API_BASE}/api/qa`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: question }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "QA request failed");
      }

      const data = await response.json();
      answerText.textContent = data.answer || "(No answer returned)";

      if (data.sources && data.sources.length > 0) {
        data.sources.forEach((src) => {
          const li = document.createElement("li");
          li.textContent = `[doc_id=${src.doc_id || "?"}] ${src.text}`;
          sourcesList.appendChild(li);
        });
      } else {
        const li = document.createElement("li");
        li.textContent = "No sources returned.";
        sourcesList.appendChild(li);
      }

      qaStatus.textContent = "Done.";
      qaStatus.classList.add("success");
    } catch (error) {
      console.error("QA error:", error);
      qaStatus.textContent = error.message || "QA request failed";
      qaStatus.classList.add("error");
    }
  });

  // Initial load
  fetchDocuments();
});

const statusPill = document.getElementById("statusPill");

const chkPdpa = document.getElementById("chkPdpa");
const chkAiDisclosed = document.getElementById("chkAiDisclosed");
const doctorName = document.getElementById("doctorName");
const btnConfirmConsent = document.getElementById("btnConfirmConsent");

const consentSection = document.getElementById("consentSection");
const recordSection = document.getElementById("recordSection");
const noteSection = document.getElementById("noteSection");

const btnStart = document.getElementById("btnStart");
const btnStop = document.getElementById("btnStop");
const recIndicator = document.getElementById("recIndicator");
const transcriptEl = document.getElementById("transcript");
const additionalDocsEl = document.getElementById("additionalDocs");
const btnGenerate = document.getElementById("btnGenerate");
const genStatus = document.getElementById("genStatus");

const noteOutput = document.getElementById("noteOutput");
const btnCopy = document.getElementById("btnCopy");
const btnPrint = document.getElementById("btnPrint");
const btnNewCase = document.getElementById("btnNewCase");

let consent = null;
let recognition = null;
let finalTranscript = "";

function setStatus(text, cls) {
  statusPill.textContent = text;
  statusPill.className = "pill " + cls;
}

btnConfirmConsent.addEventListener("click", () => {
  if (!chkPdpa.checked || !chkAiDisclosed.checked) {
    alert("Both PDPA consent and AI-use disclosure must be confirmed before continuing.");
    return;
  }
  consent = {
    patient_agreed_pdpa: true,
    ai_disclosed_to_patient: true,
    clerking_doctor: doctorName.value.trim(),
  };
  consentSection.hidden = true;
  recordSection.hidden = false;
  setStatus("Ready", "pill-idle");
});

function initRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    genStatus.textContent =
      "Live voice transcription needs Chrome or Edge. You can still type/paste the transcript manually.";
    btnStart.disabled = true;
    return null;
  }
  const rec = new SpeechRecognition();
  rec.continuous = true;
  rec.interimResults = true;
  rec.lang = "en-MY";

  rec.onresult = (event) => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const text = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += text + " ";
      } else {
        interim += text;
      }
    }
    transcriptEl.value = (finalTranscript + interim).trim();
  };

  rec.onerror = (event) => {
    console.error("Speech recognition error", event.error);
  };

  rec.onend = () => {
    if (btnStop.disabled === false) {
      // Chrome auto-stops after silence; restart while user hasn't pressed Stop.
      rec.start();
    }
  };

  return rec;
}

btnStart.addEventListener("click", () => {
  if (!recognition) recognition = initRecognition();
  if (!recognition) return;
  finalTranscript = transcriptEl.value ? transcriptEl.value + " " : "";
  recognition.start();
  btnStart.disabled = true;
  btnStop.disabled = false;
  recIndicator.hidden = false;
  setStatus("Recording", "pill-recording");
});

btnStop.addEventListener("click", () => {
  btnStop.disabled = true;
  btnStart.disabled = false;
  recIndicator.hidden = true;
  if (recognition) recognition.stop();
  setStatus("Ready", "pill-idle");
});

btnGenerate.addEventListener("click", async () => {
  if (!consent) {
    alert("Consent step missing. Please refresh and confirm consent first.");
    return;
  }
  if (!transcriptEl.value.trim()) {
    alert("Transcript is empty — record or type the clerking first.");
    return;
  }
  btnGenerate.disabled = true;
  genStatus.textContent = "Generating note…";
  setStatus("Processing", "pill-processing");

  try {
    const res = await fetch("/api/generate-note", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        transcript: transcriptEl.value,
        additional_docs: additionalDocsEl.value,
        consent,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to generate note");

    noteOutput.value = data.note;
    recordSection.hidden = true;
    noteSection.hidden = false;
    setStatus("Draft ready", "pill-done");
  } catch (err) {
    genStatus.textContent = "Error: " + err.message;
    setStatus("Ready", "pill-idle");
  } finally {
    btnGenerate.disabled = false;
  }
});

btnCopy.addEventListener("click", async () => {
  await navigator.clipboard.writeText(noteOutput.value);
  btnCopy.textContent = "Copied!";
  setTimeout(() => (btnCopy.textContent = "Copy"), 1500);
});

btnPrint.addEventListener("click", () => window.print());

btnNewCase.addEventListener("click", () => {
  finalTranscript = "";
  transcriptEl.value = "";
  additionalDocsEl.value = "";
  noteOutput.value = "";
  genStatus.textContent = "";
  chkPdpa.checked = false;
  chkAiDisclosed.checked = false;
  doctorName.value = "";
  consent = null;
  noteSection.hidden = true;
  recordSection.hidden = true;
  consentSection.hidden = false;
  setStatus("Idle", "pill-idle");
});

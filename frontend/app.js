const statusPill = document.getElementById("statusPill");

const chkPdpa = document.getElementById("chkPdpa");
const chkAiDisclosed = document.getElementById("chkAiDisclosed");
const doctorName = document.getElementById("doctorName");
const btnConfirmConsent = document.getElementById("btnConfirmConsent");

const consentSection = document.getElementById("consentSection");
const recordSection = document.getElementById("recordSection");
const noteSection = document.getElementById("noteSection");

const modeSummary = document.getElementById("modeSummary");
const modeConversation = document.getElementById("modeConversation");
const conversationModeWarning = document.getElementById("conversationModeWarning");

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
const chkDeidentified = document.getElementById("chkDeidentified");
const btnSaveExample = document.getElementById("btnSaveExample");
const saveExampleStatus = document.getElementById("saveExampleStatus");

let consent = null;
let mediaRecorder = null;
let mediaStream = null;
let audioChunks = [];
let recognition = null;
let isRecording = false;
let baseTranscript = "";
let livePreviewText = "";

function setStatus(text, cls) {
  statusPill.textContent = text;
  statusPill.className = "pill " + cls;
}

function getSelectedMode() {
  return modeConversation.checked ? "conversation" : "summary";
}

function updateModeWarning() {
  conversationModeWarning.hidden = !modeConversation.checked;
}
modeSummary.addEventListener("change", updateModeWarning);
modeConversation.addEventListener("change", updateModeWarning);

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

function pickMimeType() {
  const candidates = [
    "audio/webm;codecs=opus",
    "audio/webm",
    "audio/ogg;codecs=opus",
    "audio/ogg",
  ];
  for (const type of candidates) {
    if (window.MediaRecorder && MediaRecorder.isTypeSupported(type)) return type;
  }
  return "";
}

// Live preview only — rough, browser-based transcript shown while recording so
// there's visual feedback. Replaced entirely by the accurate local Whisper
// transcript once Stop is pressed. Not saved or sent anywhere itself.
function initRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) return null;

  const rec = new SpeechRecognition();
  rec.continuous = true;
  rec.interimResults = true;
  rec.lang = "en-MY";

  rec.onresult = (event) => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const text = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        livePreviewText += text + " ";
      } else {
        interim += text;
      }
    }
    const combined = (livePreviewText + interim).trim();
    transcriptEl.value = baseTranscript ? baseTranscript + " " + combined : combined;
  };

  rec.onerror = (event) => {
    console.error("Live preview recognition error", event.error);
  };

  rec.onend = () => {
    if (isRecording) {
      // Chrome auto-stops after silence; restart while still recording.
      try {
        rec.start();
      } catch (e) {
        // already started / race on stop - ignore
      }
    }
  };

  return rec;
}

btnStart.addEventListener("click", async () => {
  if (!window.MediaRecorder || !navigator.mediaDevices?.getUserMedia) {
    genStatus.textContent = "This browser doesn't support audio recording.";
    return;
  }
  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    genStatus.textContent = "Microphone access denied or unavailable: " + err.message;
    return;
  }

  const mimeType = pickMimeType();
  audioChunks = [];
  mediaRecorder = mimeType
    ? new MediaRecorder(mediaStream, { mimeType })
    : new MediaRecorder(mediaStream);

  mediaRecorder.ondataavailable = (event) => {
    if (event.data && event.data.size > 0) audioChunks.push(event.data);
  };

  mediaRecorder.onstop = async () => {
    mediaStream.getTracks().forEach((track) => track.stop());
    const blob = new Blob(audioChunks, { type: mediaRecorder.mimeType || "audio/webm" });
    await uploadForTranscription(blob);
  };

  isRecording = true;
  baseTranscript = transcriptEl.value.trim();
  livePreviewText = "";

  mediaRecorder.start();

  recognition = initRecognition();
  if (recognition) {
    try {
      recognition.start();
    } catch (e) {
      // ignore - live preview is best-effort only
    }
  } else {
    genStatus.textContent =
      "Live preview needs Chrome or Edge — recording still works, transcript appears after Stop.";
  }

  btnStart.disabled = true;
  btnStop.disabled = false;
  modeSummary.disabled = true;
  modeConversation.disabled = true;
  recIndicator.hidden = false;
  setStatus("Recording", "pill-recording");
});

btnStop.addEventListener("click", () => {
  btnStop.disabled = true;
  recIndicator.hidden = true;
  isRecording = false;
  if (recognition) {
    recognition.stop();
    recognition = null;
  }
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
});

async function uploadForTranscription(blob) {
  setStatus("Transcribing", "pill-processing");
  genStatus.textContent = "Transcribing audio…";
  btnGenerate.disabled = true;

  try {
    const formData = new FormData();
    const ext = (mediaRecorder.mimeType || "audio/webm").includes("ogg") ? "ogg" : "webm";
    formData.append("audio", blob, `recording.${ext}`);
    formData.append("patient_agreed_pdpa", String(consent.patient_agreed_pdpa));
    formData.append("ai_disclosed_to_patient", String(consent.ai_disclosed_to_patient));

    const res = await fetch("/api/transcribe", { method: "POST", body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to transcribe audio");

    // Replace the rough live-preview text with the accurate Whisper transcript.
    transcriptEl.value = baseTranscript ? baseTranscript + " " + data.transcript : data.transcript;
    genStatus.textContent = "Transcription complete — review/edit above before generating.";
    setStatus("Ready", "pill-idle");
  } catch (err) {
    genStatus.textContent = "Error: " + err.message;
    setStatus("Ready", "pill-idle");
  } finally {
    btnStart.disabled = false;
    modeSummary.disabled = false;
    modeConversation.disabled = false;
    btnGenerate.disabled = false;
  }
}

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
        mode: getSelectedMode(),
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

btnSaveExample.addEventListener("click", async () => {
  if (!chkDeidentified.checked) {
    alert("Please confirm the example is de-identified before saving it for training.");
    return;
  }
  btnSaveExample.disabled = true;
  saveExampleStatus.textContent = "Saving…";
  try {
    const res = await fetch("/api/training-examples", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        transcript: transcriptEl.value,
        additional_docs: additionalDocsEl.value,
        final_note: noteOutput.value,
        deidentified_confirmed: chkDeidentified.checked,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to save example");
    saveExampleStatus.textContent = `Saved. Total examples so far: ${data.total_examples}`;
    chkDeidentified.checked = false;
  } catch (err) {
    saveExampleStatus.textContent = "Error: " + err.message;
  } finally {
    btnSaveExample.disabled = false;
  }
});

btnNewCase.addEventListener("click", () => {
  audioChunks = [];
  isRecording = false;
  baseTranscript = "";
  livePreviewText = "";
  if (recognition) {
    recognition.stop();
    recognition = null;
  }
  transcriptEl.value = "";
  additionalDocsEl.value = "";
  noteOutput.value = "";
  genStatus.textContent = "";
  chkPdpa.checked = false;
  chkAiDisclosed.checked = false;
  doctorName.value = "";
  modeSummary.checked = true;
  updateModeWarning();
  consent = null;
  noteSection.hidden = true;
  recordSection.hidden = true;
  consentSection.hidden = false;
  setStatus("Idle", "pill-idle");
});

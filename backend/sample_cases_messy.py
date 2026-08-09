"""5 additional synthetic cases (on top of the 10 in seed_training_data.py),
this time simulating REALISTIC messy speech-to-text output — garbled
abbreviations, mis-heard drug names, dictation self-corrections — the kind of
thing that broke the model in real testing (e.g. "23 ABF" instead of "leads
II, III, aVF", "ECS" instead of "ACS"). The reference final_note in each case
demonstrates the CORRECT handling per the "never invent a fix, preserve or
flag instead" rule: ambiguous fragments are kept verbatim or marked
"[unclear: ...]" and called out in FLAGS FOR DOCTOR, never confidently
reinterpreted. All patients are fictional.
"""

CASES = [
    {
        "label": "Inferior STEMI (garbled ECG leads + abbreviation + drug names)",
        "transcript": (
            "This patient is 55 years old gentleman with known case of hypertension and "
            "diabetes. He complained of chest pain since past three days associated with "
            "diaphoresis, palpitation, and reduced effort tolerance. Otherwise no fever, "
            "no cough, no URT symptoms, no vomiting as well. On examination, alert "
            "conscious, good pulse volume, CRT was less than 2 seconds, one periphery, "
            "water size table, BP is 120 over 80, heart rate is 20, 57. ECT showed ST "
            "elevation at 23 ABF. So the impression now is ECS with STEMI. Plan is to "
            "refer IJN for angiogram and to serve dual anti-platelet TAP aspirin 300 mg "
            "stat and TAP Flavix 300 mg stat on interviter signs every 15 minutes to "
            "inform in patient's condition."
        ),
        "additional_docs": "",
        "final_note": """PATIENT PARTICULARS
Name: Not mentioned | Age/Sex: 55M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Chest pain, 3 days duration.

HISTORY OF PRESENTING ILLNESS (HOPI)
Chest pain for the past 3 days, associated with diaphoresis, palpitations, and
reduced effort tolerance. No fever, no cough, no upper respiratory tract
symptoms, no vomiting.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Known hypertension and diabetes mellitus.

DRUG HISTORY & ALLERGIES (DHx)
Not mentioned.

SOCIAL HISTORY (SHx)
Not mentioned.

PHYSICAL EXAMINATION (PE)
BP 120/80 mmHg, HR 57 bpm. Alert and conscious, good pulse volume, CRT < 2
seconds, peripheries warm. [unclear: "water size table" — likely a
transcription artifact; meaning unclear, please confirm]

INVESTIGATIONS
ECG: ST elevation reported at "23 ABF" [unclear — likely intended as leads
II, III, aVF, but transcribed ambiguously; please confirm].

DIAGNOSIS / CLINICAL IMPRESSION
Impression: "ECS" with STEMI [unclear — likely intended as ACS (Acute
Coronary Syndrome), but transcribed ambiguously; please confirm].

MANAGEMENT PLAN
Referred to IJN for angiogram. Dual antiplatelet therapy: Tab Aspirin 300mg
stat, Tab [unclear: "Flavix" — likely Plavix (clopidogrel); please confirm]
300mg stat. [unclear: "on interviter signs every 15 minutes to inform in
patient's condition" — likely intended as monitor vital signs every 15
minutes; please confirm].

DISPOSITION
Not mentioned (admission implied by angiogram referral, not stated
explicitly).

FLAGS FOR DOCTOR
- Several likely transcription errors marked [unclear] above — please verify:
  ECG lead description, diagnosis abbreviation, and antiplatelet drug name.
- Respiratory rate, SpO2, temperature, and GCS not mentioned.
- Drug allergy status not mentioned.
- Disposition (ward/admission) not explicitly stated.""",
    },
    {
        "label": "MVA head injury (unconfirmed negative + missing CT brain flag)",
        "transcript": (
            "Alleged MVA, motorbike versus pedestrian. Patient sustained abrasion wound "
            "over the right arm, unable to move the right arm, ada swelling. Then he had "
            "LOC followed by projectile vomiting. On examination, abdomen soft and "
            "tender, pupils five mil reactive to light bilaterally, normal PR, good "
            "chest expansion, breath sounds equal bilaterally on auscultation. Right arm "
            "unable to move due to swelling, deformity noted. Plan, refer right arm for "
            "x-ray, give analgesia."
        ),
        "additional_docs": "",
        "final_note": """PATIENT PARTICULARS
Name: Not mentioned | Age/Sex: Not mentioned | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Alleged motor vehicle accident (MVA), motorbike versus pedestrian.

HISTORY OF PRESENTING ILLNESS (HOPI)
Sustained abrasion wound over right arm, unable to move right arm with
associated swelling. Reported loss of consciousness (LOC) followed by
projectile vomiting. Other injuries: not mentioned — full secondary survey
not confirmed.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Not mentioned.

DRUG HISTORY & ALLERGIES (DHx)
Not mentioned.

SOCIAL HISTORY (SHx)
Not mentioned.

PHYSICAL EXAMINATION (PE)
BP, HR, RR, SpO2, Temp, GCS: not mentioned. Abdomen soft and tender. Pupils
5mm, reactive to light bilaterally. PR exam normal. Good chest expansion,
breath sounds equal bilaterally. Right arm: unable to move, swelling and
deformity noted.

INVESTIGATIONS
None mentioned.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Suspected right arm fracture (clinical suspicion; pending
X-ray). Query significant head injury given reported LOC and vomiting — not
otherwise characterized.

MANAGEMENT PLAN
Right arm X-ray requested. Analgesia given (specific agent/dose not
mentioned).

DISPOSITION
Not mentioned.

FLAGS FOR DOCTOR
- GCS not documented despite reported LOC — should be assessed and recorded.
- No CT brain or neuro-observation plan documented despite LOC + projectile
  vomiting (red flags for significant head injury / raised ICP) — recommend
  urgent review.
- Vitals (BP, HR, RR, SpO2, Temp) not documented.
- "Other injuries: not mentioned" — do not assume none exist; full injury
  survey not explicitly confirmed as completed.
- Analgesia given but specific drug/dose not documented.""",
    },
    {
        "label": "Severe CAP with septic shock (garbled drug name + drowsy-no-GCS)",
        "transcript": (
            "Encik Zainal, 68, known diabetic and hypertensive, presented with fever and "
            "cough for four days, today more drowsy, family noticed reduced oral intake. "
            "On examination, patient look toxic, BP eighty over fifty, hear rate one "
            "thirty two, respiratory rate thirty four, sats eighty eight percent room "
            "air, temp thirty nine point five. Reduced air entry left lower zone. Given "
            "IV normal saline bolus, IV Rosephin two gram stat, oxygen via face mask. "
            "Impression severe CAP with sepsis, likely septic shock. For ICU referral."
        ),
        "additional_docs": "CXR: left lower zone consolidation.",
        "final_note": """PATIENT PARTICULARS
Name: Encik Zainal | Age/Sex: 68M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Fever and cough, 4 days duration, with new drowsiness today.

HISTORY OF PRESENTING ILLNESS (HOPI)
Fever and cough for 4 days. Increasing drowsiness today, with reduced oral
intake noted by family.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Diabetes mellitus, hypertension.

DRUG HISTORY & ALLERGIES (DHx)
Not mentioned.

SOCIAL HISTORY (SHx)
Not mentioned.

PHYSICAL EXAMINATION (PE)
BP 80/50 mmHg, HR 132 bpm, RR 34/min, SpO2 88% on room air, T 39.5°C.
Patient toxic-looking. Reduced air entry left lower zone.

INVESTIGATIONS
CXR: left lower zone consolidation.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Severe community-acquired pneumonia (CAP) with sepsis, likely
septic shock.

MANAGEMENT PLAN
IV Normal Saline bolus given. IV [unclear: "Rosephin" — likely Rocephin
(ceftriaxone); please confirm exact drug and dose] 2g stat given. Oxygen via
face mask. For ICU referral.

DISPOSITION
For ICU referral / admission.

FLAGS FOR DOCTOR
- GCS not formally scored despite "more drowsy" being reported — should be
  assessed and recorded given possible septic encephalopathy.
- Drug name "Rosephin" needs confirmation (likely Rocephin/ceftriaxone).
- Lactate and blood cultures not mentioned — relevant for sepsis workup,
  ideally taken before antibiotics.
- Allergy status not mentioned.""",
    },
    {
        "label": "New atrial fibrillation (dictation self-correction, drug name)",
        "transcript": (
            "Puan Chong, 74, presented with palpitations and giddiness since this "
            "morning, known ischemic heart disease. ECG showed irregular irregular "
            "rhythm, no P wave, rate one ten, in keeping with AF, af. Started on tablet "
            "the loquis, sorry, eloquis 5 mg BD and tablet bisoprolol two point five mg "
            "OD. Referred cardiology for further workup."
        ),
        "additional_docs": "",
        "final_note": """PATIENT PARTICULARS
Name: Puan Chong | Age/Sex: 74F | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Palpitations and giddiness since this morning.

HISTORY OF PRESENTING ILLNESS (HOPI)
Palpitations and giddiness, onset this morning. Known ischemic heart
disease.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Ischemic heart disease.

DRUG HISTORY & ALLERGIES (DHx)
Not mentioned.

SOCIAL HISTORY (SHx)
Not mentioned.

PHYSICAL EXAMINATION (PE)
Vitals (BP, HR, RR, SpO2, Temp, GCS) not mentioned beyond ECG findings
below.

INVESTIGATIONS
ECG: irregularly irregular rhythm, no P waves, rate ~110/min — in keeping
with atrial fibrillation.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: New atrial fibrillation.

MANAGEMENT PLAN
Tab [unclear: transcribed as "the loquis, sorry, eloquis" — appears to be a
self-correction during dictation, likely intended as Eliquis (apixaban);
please verify exact drug name and dose] 5mg BD started. Tab Bisoprolol
2.5mg OD started. Cardiology referral made.

DISPOSITION
Not mentioned.

FLAGS FOR DOCTOR
- Anticoagulant drug name needs confirmation (transcribed ambiguously as
  "the loquis, sorry, eloquis").
- Stroke risk assessment (e.g. CHA2DS2-VASc) and bleeding risk not
  mentioned — relevant before starting anticoagulation for new AF.
- Vitals not documented.""",
    },
    {
        "label": "Post-ictal seizure (ambiguous dose self-correction)",
        "transcript": (
            "This is a 30 year old lady, known epileptic, brought in post seizure "
            "episode, witnessed generalized tonic clonic seizure lasting about two "
            "minutes, now postictal, drowsy but rousable. On regular tablet carba, "
            "carbamazepine two hundred mg, sorry two hundred BD. Given IV diazepam five "
            "mg stat for the seizure. Vitals BP one ten over seventy, pulse ninety, "
            "sats ninety nine percent, temp thirty seven. Plan for neuro review and old "
            "note tracing, observe in ward."
        ),
        "additional_docs": "",
        "final_note": """PATIENT PARTICULARS
Name: Not mentioned | Age/Sex: 30F | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Post-seizure episode, brought in postictal.

HISTORY OF PRESENTING ILLNESS (HOPI)
Known epileptic. Witnessed generalized tonic-clonic seizure lasting ~2
minutes. Now postictal, drowsy but rousable.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Epilepsy.

DRUG HISTORY & ALLERGIES (DHx)
Regular Tab Carbamazepine [unclear: dose/frequency transcribed as "two
hundred mg, sorry two hundred BD" — appears self-corrected during dictation
but remains ambiguous; please confirm exact dose and frequency]. Allergies
not mentioned.

SOCIAL HISTORY (SHx)
Not mentioned.

PHYSICAL EXAMINATION (PE)
BP 110/70 mmHg, HR 90 bpm, SpO2 99% on room air, T 37.0°C. Drowsy but
rousable (postictal); GCS not formally scored.

INVESTIGATIONS
None mentioned.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Post-ictal state following witnessed generalized tonic-clonic
seizure, known epilepsy.

MANAGEMENT PLAN
IV Diazepam 5mg stat given for the seizure. For neuro review and retrieval
of old clinical notes/records. Observe in ward.

DISPOSITION
Observe in ward.

FLAGS FOR DOCTOR
- GCS not formally scored — only descriptive "drowsy but rousable"
  documented; should be scored given postictal state.
- Carbamazepine dose/frequency ambiguous per transcription ("two hundred
  mg, sorry two hundred BD") — please confirm exact regular dose.
- Allergy status not mentioned.
- Seizure trigger / precipitant (e.g. medication compliance, missed doses)
  not explored in the transcript.""",
    },
]

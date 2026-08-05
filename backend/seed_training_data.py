"""One-off script: seeds data/training_examples.jsonl with 10 synthetic
(transcript, additional_docs, final_note) cases (5 non-trauma, 5 trauma).
All patients are fictional — safe to load as-is.

Run inside the container:
    docker compose exec app python seed_training_data.py
"""
from training_data import save_example

CASES = [
    {
        "label": "STEMI (chest pain)",
        "transcript": (
            "Patient Encik Rahman, 52 year old male, presented with central chest pain for "
            "3 hours, radiating to the left arm and jaw, associated with sweating and "
            "nausea. No known medical illness, no known drug allergy. Smoker, 20 pack "
            "years. On examination patient looks unwell and diaphoretic, blood pressure "
            "160 over 95, heart rate 105, respiratory rate 22, saturation 96% on room "
            "air, temperature 37.1. Heart sounds normal, lungs clear. ECG shows ST "
            "elevation in leads 2, 3, AVF. Troponin sent. Impression is inferior STEMI, "
            "given aspirin 300mg, clopidogrel 300mg loading dose, for urgent "
            "thrombolysis, referring cardiology, admit CCU."
        ),
        "additional_docs": (
            "ECG: ST elevation leads II, III, aVF, reciprocal depression in aVL.\n"
            "Troponin I: pending.\n"
            "Given: Tab Aspirin 300mg stat, Tab Clopidogrel 300mg stat, IV Morphine 3mg stat."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Encik Rahman | Age/Sex: 52M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Central chest pain, 3 hours duration.

HISTORY OF PRESENTING ILLNESS (HOPI)
Central chest pain radiating to left arm and jaw, associated with diaphoresis
and nausea. Onset 3 hours prior to arrival. No prior similar episodes mentioned.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
No known medical illness (NKMI).

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA). No regular medications mentioned.

SOCIAL HISTORY (SHx)
Smoker, 20 pack-year history.

PHYSICAL EXAMINATION (PE)
BP 160/95 mmHg, HR 105 bpm, RR 22/min, SpO2 96% on room air, T 37.1°C.
Patient diaphoretic and unwell-looking. Heart sounds normal, lungs clear
bilaterally.

INVESTIGATIONS
ECG: ST elevation in leads II, III, aVF with reciprocal depression in aVL.
Troponin I: pending.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Inferior STEMI.

MANAGEMENT PLAN
Tab Aspirin 300mg stat, Tab Clopidogrel 300mg loading dose, IV Morphine 3mg
stat given. For urgent thrombolysis. Cardiology referral made.

DISPOSITION
Admit to CCU.

FLAGS FOR DOCTOR
- GCS not mentioned.
- Troponin result pending at time of clerking.""",
    },
    {
        "label": "Acute severe asthma",
        "transcript": (
            "Cik Aminah, 24 year old female, known asthmatic since childhood, presented "
            "with worsening shortness of breath and wheezing for 1 day, triggered by "
            "upper respiratory tract infection symptoms 2 days ago. Using salbutamol "
            "inhaler at home but not improving. No known drug allergy. Non-smoker. On "
            "examination patient tachypnoeic, able to speak in short phrases only, "
            "using accessory muscles. Blood pressure 128 over 80, heart rate 118, "
            "respiratory rate 28, saturation 93% on room air, temperature 37.4. Bilateral "
            "widespread wheeze on auscultation, no crepitations. Given back to back "
            "nebulizer salbutamol and ipratropium, IV hydrocortisone. Impression acute "
            "severe asthma exacerbation, for admission, observe response to treatment."
        ),
        "additional_docs": (
            "Peak flow: 45% predicted.\n"
            "Given: Neb Salbutamol 5mg + Ipratropium 500mcg back-to-back x3, "
            "IV Hydrocortisone 200mg stat.\n"
            "CXR: no consolidation, hyperinflated lung fields."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Cik Aminah | Age/Sex: 24F | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Worsening shortness of breath and wheezing, 1 day duration.

HISTORY OF PRESENTING ILLNESS (HOPI)
Known asthmatic since childhood. Worsening dyspnoea and wheeze over 1 day,
triggered by URTI symptoms starting 2 days prior. Using home salbutamol
inhaler without improvement.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Bronchial asthma since childhood.

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA). Regular salbutamol inhaler (PRN, home use).

SOCIAL HISTORY (SHx)
Non-smoker.

PHYSICAL EXAMINATION (PE)
BP 128/80 mmHg, HR 118 bpm, RR 28/min, SpO2 93% on room air, T 37.4°C.
Tachypnoeic, able to speak in short phrases only, using accessory muscles.
Bilateral widespread wheeze on auscultation, no crepitations.

INVESTIGATIONS
Peak flow: 45% predicted.
CXR: no consolidation, hyperinflated lung fields.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Acute severe asthma exacerbation, likely URTI-triggered.

MANAGEMENT PLAN
Nebulized Salbutamol 5mg + Ipratropium 500mcg back-to-back x3, IV
Hydrocortisone 200mg stat given. Observe response to treatment.

DISPOSITION
Admit for observation and further bronchodilator therapy.

FLAGS FOR DOCTOR
- GCS not mentioned.
- Baseline (personal best) peak flow not mentioned for comparison.""",
    },
    {
        "label": "Diabetic ketoacidosis",
        "transcript": (
            "Encik Suresh, 34 year old male, known type 1 diabetic, presented with "
            "vomiting and abdominal pain for 1 day, and noted to be breathing fast. "
            "Family says he ran out of insulin 3 days ago. No known drug allergy. "
            "Non-smoker, non-drinker. On examination patient drowsy but rousable, "
            "dehydrated, blood pressure 100 over 60, heart rate 122, respiratory rate 32 "
            "deep and sighing, saturation 98% room air, temperature 37.0. Capillary "
            "blood glucose reading hi, unable to read on glucometer. Ketones positive "
            "in urine. Started on IV fluids and insulin infusion protocol. Impression "
            "diabetic ketoacidosis secondary to insulin omission, for admission medical "
            "ward, close monitoring."
        ),
        "additional_docs": (
            "CBG: HI (>27.8 mmol/L)\n"
            "Urine ketones: 3+\n"
            "VBG: pH 7.05, HCO3 8 mmol/L\n"
            "Given: IV Normal Saline bolus, IV Actrapid infusion per DKA protocol, "
            "hourly CBG monitoring."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Encik Suresh | Age/Sex: 34M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Vomiting and abdominal pain, 1 day duration, with fast breathing.

HISTORY OF PRESENTING ILLNESS (HOPI)
Known type 1 diabetic. Ran out of insulin 3 days prior to presentation.
Developed vomiting, abdominal pain over 1 day, with subsequent fast/deep
breathing noted by family.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Type 1 diabetes mellitus.

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA). Regular insulin (defaulted x3 days prior to
presentation).

SOCIAL HISTORY (SHx)
Non-smoker, non-drinker.

PHYSICAL EXAMINATION (PE)
BP 100/60 mmHg, HR 122 bpm, RR 32/min (deep and sighing/Kussmaul), SpO2 98%
on room air, T 37.0°C. Drowsy but rousable, clinically dehydrated.

INVESTIGATIONS
CBG: HI (>27.8 mmol/L). Urine ketones: 3+. VBG: pH 7.05, HCO3 8 mmol/L.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Diabetic ketoacidosis, secondary to insulin omission.

MANAGEMENT PLAN
IV Normal Saline bolus given. IV Actrapid infusion started per DKA protocol.
Hourly capillary blood glucose monitoring.

DISPOSITION
Admit to medical ward for close monitoring.

FLAGS FOR DOCTOR
- GCS not explicitly scored (only "drowsy but rousable" documented).
- Serum electrolytes (K+) not mentioned — required before/during insulin
  infusion.""",
    },
    {
        "label": "Acute ischaemic stroke",
        "transcript": (
            "Cik Fatimah, 68 year old female, known hypertensive and diabetic, brought "
            "in by family after they noticed sudden right-sided weakness and slurred "
            "speech while having breakfast, last seen normal 1 hour ago. No known drug "
            "allergy. On examination patient alert, GCS 15, blood pressure 178 over 98, "
            "heart rate 88 irregular, respiratory rate 18, saturation 97% room air, "
            "temperature 36.8. Right upper and lower limb power 2 out of 5, facial "
            "asymmetry with right sided droop, speech slurred. CT brain done, no bleed "
            "seen. Within thrombolysis window. Impression acute ischaemic stroke, for "
            "thrombolysis workup, referred neurology urgently."
        ),
        "additional_docs": (
            "CT brain (plain): no acute haemorrhage, no established infarct yet visualized.\n"
            "ECG: irregularly irregular rhythm, no clear P waves - ?atrial fibrillation.\n"
            "Last seen normal: 1 hour prior to arrival."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Cik Fatimah | Age/Sex: 68F | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Sudden right-sided weakness and slurred speech, onset 1 hour prior to
arrival (last seen normal).

HISTORY OF PRESENTING ILLNESS (HOPI)
Sudden onset right-sided limb weakness and slurred speech noticed by family
during breakfast. Last seen normal 1 hour prior to arrival. Brought in
immediately by family.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Hypertension, diabetes mellitus.

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
GCS 15. BP 178/98 mmHg, HR 88 irregular, RR 18/min, SpO2 97% on room air,
T 36.8°C. Right upper and lower limb power 2/5. Right-sided facial droop.
Slurred speech.

INVESTIGATIONS
CT brain (plain): no acute haemorrhage. ECG: irregularly irregular rhythm,
no clear P waves, suspicious for atrial fibrillation.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Acute ischaemic stroke, within thrombolysis window. Possible
underlying atrial fibrillation.

MANAGEMENT PLAN
For thrombolysis workup. Urgent neurology referral made.

DISPOSITION
Pending neurology assessment — for likely stroke unit / ICU admission.

FLAGS FOR DOCTOR
- Blood glucose (CBG) not mentioned — mandatory to exclude hypoglycaemia as
  stroke mimic before thrombolysis.
- Weight not mentioned — required for thrombolysis dosing.""",
    },
    {
        "label": "CAP with sepsis",
        "transcript": (
            "Encik Tan, 71 year old male, presented with fever and cough with "
            "yellowish sputum for 4 days, and increasing confusion noted by daughter "
            "today. Known hypertensive. No known drug allergy. On examination patient "
            "looks lethargic, disoriented to time, blood pressure 88 over 54, heart "
            "rate 128, respiratory rate 30, saturation 89% on room air improved to 94% "
            "on 4 litre nasal prongs, temperature 39.2. Reduced air entry right lower "
            "zone with crepitations. Impression community acquired pneumonia with "
            "sepsis, started on IV fluids, IV antibiotics, oxygen, for admission, "
            "close monitoring, referred medical team."
        ),
        "additional_docs": (
            "CXR: right lower zone consolidation.\n"
            "FBC: WBC 18.5, sepsis screen sent.\n"
            "Lactate: 3.8 mmol/L\n"
            "Given: IV Normal Saline 500ml bolus, IV Ceftriaxone 2g stat, "
            "O2 via nasal prongs 4L/min."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Encik Tan | Age/Sex: 71M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Fever and productive cough, 4 days duration, with new confusion today.

HISTORY OF PRESENTING ILLNESS (HOPI)
Fever and cough productive of yellowish sputum for 4 days. Increasing
confusion noted by daughter on day of presentation.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Hypertension.

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
BP 88/54 mmHg, HR 128 bpm, RR 30/min, SpO2 89% on room air (94% on 4L nasal
prongs), T 39.2°C. Lethargic, disoriented to time. Reduced air entry right
lower zone with crepitations.

INVESTIGATIONS
CXR: right lower zone consolidation. FBC: WBC 18.5. Lactate: 3.8 mmol/L.
Sepsis screen sent.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Community-acquired pneumonia with sepsis.

MANAGEMENT PLAN
IV Normal Saline 500ml bolus given. IV Ceftriaxone 2g stat given. Oxygen
via nasal prongs 4L/min. Medical team referral made.

DISPOSITION
Admit for further management and close monitoring, sepsis protocol.

FLAGS FOR DOCTOR
- GCS not explicitly scored (only "disoriented to time" documented).
- Blood cultures not explicitly mentioned as taken before antibiotics.""",
    },
    {
        "label": "RTA polytrauma",
        "transcript": (
            "Encik Faizal, 29 year old male, motorcyclist involved in high speed road "
            "traffic accident, brought in by ambulance with cervical collar and spinal "
            "board. Complains of chest pain and right leg pain. No loss of consciousness "
            "per patient. No known medical illness, no known drug allergy. On "
            "examination patient alert, GCS 15, blood pressure 105 over 70, heart rate "
            "115, respiratory rate 24, saturation 95% room air, temperature 36.9. "
            "Tenderness over right lower chest wall, no crepitus. Right thigh deformity "
            "and swelling, distal pulses present. Abdomen soft, no guarding. Primary "
            "survey ABCDE done, no airway or breathing compromise. Impression right "
            "femur fracture, possible right rib fracture, for trauma imaging, ortho and "
            "surgical referral."
        ),
        "additional_docs": (
            "FAST scan: no free fluid.\n"
            "CXR: query right 8th-9th rib fracture, no pneumothorax.\n"
            "X-ray right femur: mid-shaft fracture.\n"
            "Given: IV Morphine 5mg for analgesia, right leg splinted."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Encik Faizal | Age/Sex: 29M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Chest pain and right leg pain following high-speed motorcycle road traffic
accident.

HISTORY OF PRESENTING ILLNESS (HOPI)
Motorcyclist involved in high-speed RTA. Brought in by ambulance with
cervical collar and spinal board precautions. No loss of consciousness
reported by patient. Chest pain and right leg pain since the accident.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
No known medical illness (NKMI).

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
GCS 15. BP 105/70 mmHg, HR 115 bpm, RR 24/min, SpO2 95% on room air, T
36.9°C. Primary survey (ABCDE) — no airway or breathing compromise.
Tenderness over right lower chest wall, no crepitus. Right thigh deformity
and swelling, distal pulses present. Abdomen soft, no guarding.

INVESTIGATIONS
FAST scan: no free fluid. CXR: query right 8th-9th rib fracture, no
pneumothorax. X-ray right femur: mid-shaft fracture.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Right femur mid-shaft fracture; possible right rib fracture(s).
Polytrauma post-RTA.

MANAGEMENT PLAN
IV Morphine 5mg given for analgesia. Right leg splinted. For trauma
imaging series. Orthopaedic and general surgical referral made.

DISPOSITION
Pending ortho/surgical assessment — likely admission.

FLAGS FOR DOCTOR
- C-spine clearance status not explicitly documented despite collar in situ.
- Tetanus status not mentioned.""",
    },
    {
        "label": "Hip fracture from fall",
        "transcript": (
            "Cik Zainab, 78 year old female, fell from standing height at home this "
            "morning, unable to bear weight on left leg afterwards. Known hypertensive "
            "and osteoporosis. No known drug allergy. On examination patient alert, "
            "GCS 15, blood pressure 138 over 82, heart rate 92, respiratory rate 18, "
            "saturation 97% room air, temperature 36.7. Left leg shortened and "
            "externally rotated, tenderness over left hip, unable to straight leg "
            "raise. No other injuries noted. Impression left neck of femur fracture, "
            "given analgesia, for X-ray, orthopaedic referral, admission."
        ),
        "additional_docs": (
            "X-ray left hip: fracture neck of femur, displaced.\n"
            "Given: IV Paracetamol 1g, IV Morphine 2mg titrated."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Cik Zainab | Age/Sex: 78F | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Left hip pain and inability to bear weight following a fall at home.

HISTORY OF PRESENTING ILLNESS (HOPI)
Fell from standing height at home this morning. Unable to bear weight on
left leg since the fall.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
Hypertension, osteoporosis.

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
GCS 15. BP 138/82 mmHg, HR 92 bpm, RR 18/min, SpO2 97% on room air, T
36.7°C. Left leg shortened and externally rotated. Tenderness over left
hip. Unable to straight leg raise. No other injuries noted.

INVESTIGATIONS
X-ray left hip: displaced fracture neck of femur.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Left displaced neck of femur fracture, post mechanical fall.

MANAGEMENT PLAN
IV Paracetamol 1g given. IV Morphine 2mg titrated for analgesia.
Orthopaedic referral made.

DISPOSITION
Admit under orthopaedics for surgical management.

FLAGS FOR DOCTOR
- Cause of fall (mechanical vs. syncope/collapse) not clearly established —
  relevant given age.
- Anticoagulant/antiplatelet use not mentioned — relevant for surgical
  planning.""",
    },
    {
        "label": "Penetrating trauma, stab wound",
        "transcript": (
            "Encik Kumar, 31 year old male, alleged stabbed by unknown assailant, single "
            "stab wound to left upper abdomen, about 30 minutes ago. No known medical "
            "illness, no known drug allergy. On examination patient alert, GCS 15, "
            "anxious, blood pressure 98 over 62, heart rate 122, respiratory rate 24, "
            "saturation 96% room air, temperature 36.8. Single stab wound left "
            "hypochondrium approximately 3cm, active minor bleeding, abdomen tender "
            "with guarding. No exit wound seen. Impression penetrating abdominal trauma, "
            "haemodynamically borderline, activated massive transfusion protocol on "
            "standby, for urgent surgical exploration, informed surgical team and "
            "police report to be made."
        ),
        "additional_docs": (
            "FAST scan: free fluid in Morrison's pouch.\n"
            "Group and crossmatch sent, 4 units.\n"
            "Given: IV Normal Saline wide bore access x2, wound covered with dressing."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Encik Kumar | Age/Sex: 31M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Single stab wound to left upper abdomen, approximately 30 minutes prior to
arrival.

HISTORY OF PRESENTING ILLNESS (HOPI)
Alleged assault by unknown assailant, single stab wound sustained to left
upper abdomen ~30 minutes prior to arrival.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
No known medical illness (NKMI).

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
GCS 15, anxious. BP 98/62 mmHg, HR 122 bpm, RR 24/min, SpO2 96% on room
air, T 36.8°C. Single stab wound left hypochondrium ~3cm with active minor
bleeding. No exit wound seen. Abdomen tender with guarding.

INVESTIGATIONS
FAST scan: free fluid in Morrison's pouch. Group and crossmatch sent (4
units).

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Penetrating abdominal trauma (stab wound), haemodynamically
borderline, positive FAST — concern for intra-abdominal haemorrhage.

MANAGEMENT PLAN
IV wide-bore access x2 obtained, IV Normal Saline given. Wound covered
with dressing. Massive transfusion protocol placed on standby. Surgical
team informed for urgent exploration. Medico-legal/police report to be
made per protocol.

DISPOSITION
For emergency operating theatre — urgent surgical exploration.

FLAGS FOR DOCTOR
- Tetanus status not mentioned.
- Exact time of assault vs. arrival should be documented precisely for
  medico-legal purposes.""",
    },
    {
        "label": "Head injury, motorcycle accident",
        "transcript": (
            "Encik Hafiz, 22 year old male, motorcyclist, fell off bike at moderate "
            "speed, hit head on road, was wearing helmet. Brief loss of consciousness "
            "witnessed by friend, about 1 minute. Now complaining of headache and "
            "vomited once. No known medical illness, no known drug allergy. On "
            "examination patient alert, GCS 14, E3V5M6, blood pressure 132 over 84, "
            "heart rate 78, respiratory rate 16, saturation 99% room air, temperature "
            "36.6. Small laceration over left forehead, no active bleeding. Pupils "
            "equal and reactive. No focal neurological deficit. Neck examination "
            "unremarkable, no midline tenderness. Impression mild traumatic brain "
            "injury, for CT brain, neuro observation, admission for monitoring."
        ),
        "additional_docs": (
            "CT brain: pending at time of clerking.\n"
            "GCS trend: 15 at scene per ambulance crew, 14 on arrival.\n"
            "Given: wound cleaned and dressed, analgesia IV Paracetamol 1g."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Encik Hafiz | Age/Sex: 22M | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Head injury with brief loss of consciousness following a motorcycle fall.

HISTORY OF PRESENTING ILLNESS (HOPI)
Motorcyclist, fell off bike at moderate speed, helmeted, struck head on
road. Witnessed brief loss of consciousness (~1 minute). Headache and one
episode of vomiting since the fall. GCS 15 at scene per ambulance crew,
14 on arrival (E3V5M6).

PAST MEDICAL / SURGICAL HISTORY (PMHx)
No known medical illness (NKMI).

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
GCS 14 (E3V5M6). BP 132/84 mmHg, HR 78 bpm, RR 16/min, SpO2 99% on room
air, T 36.6°C. Small left forehead laceration, no active bleeding. Pupils
equal and reactive. No focal neurological deficit. Neck: no midline
tenderness.

INVESTIGATIONS
CT brain: pending at time of clerking.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Mild traumatic brain injury (GCS drop from 15 to 14), post
motorcycle accident.

MANAGEMENT PLAN
Wound cleaned and dressed. IV Paracetamol 1g given for analgesia. For CT
brain. Neuro-observation charting.

DISPOSITION
Admit for neuro-observation and monitoring pending CT brain result.

FLAGS FOR DOCTOR
- C-spine clearance not explicitly documented despite mechanism of injury.
- Anticoagulant/antiplatelet use not mentioned — relevant given head
  injury.""",
    },
    {
        "label": "Burns, house fire",
        "transcript": (
            "Cik Mei Ling, 40 year old female, sustained burns from house fire "
            "approximately 1 hour ago, flame burns to both arms and anterior chest. "
            "Was in an enclosed room briefly before escaping. No known medical illness, "
            "no known drug allergy. On examination patient alert, GCS 15, mild hoarseness "
            "of voice, no soot noted in mouth or nostrils, blood pressure 118 over 76, "
            "heart rate 108, respiratory rate 22, saturation 97% room air, temperature "
            "36.9. Partial thickness burns estimated 18% total body surface area "
            "involving both forearms and anterior chest, blistering present. No "
            "circumferential burns. Impression partial thickness burns 18% TBSA with "
            "possible inhalational injury risk given enclosed space exposure, for burns "
            "protocol fluid resuscitation, referred burns unit."
        ),
        "additional_docs": (
            "TBSA estimated: 18% (Rule of Nines).\n"
            "Parkland formula fluid calculation to be applied.\n"
            "Given: IV Normal Saline per burns protocol, wounds covered with cling "
            "film, analgesia IV Morphine 5mg."
        ),
        "final_note": """PATIENT PARTICULARS
Name: Cik Mei Ling | Age/Sex: 40F | Triage Zone: Green Zone

PRESENTING COMPLAINT (PC)
Flame burns to both arms and anterior chest, ~1 hour prior to arrival.

HISTORY OF PRESENTING ILLNESS (HOPI)
Sustained flame burns during a house fire approximately 1 hour ago. Brief
exposure in an enclosed room before escaping. Mild hoarseness of voice
noted since the incident.

PAST MEDICAL / SURGICAL HISTORY (PMHx)
No known medical illness (NKMI).

DRUG HISTORY & ALLERGIES (DHx)
No known drug allergy (NKDA).

SOCIAL HISTORY (SHx)
Not mentioned / not assessed.

PHYSICAL EXAMINATION (PE)
GCS 15. BP 118/76 mmHg, HR 108 bpm, RR 22/min, SpO2 97% on room air, T
36.9°C. Mild hoarseness of voice. No soot noted in mouth or nostrils.
Partial thickness burns ~18% TBSA (Rule of Nines) involving both forearms
and anterior chest, with blistering. No circumferential burns.

INVESTIGATIONS
TBSA estimated 18% (Rule of Nines). Parkland formula fluid calculation to
be applied.

DIAGNOSIS / CLINICAL IMPRESSION
Impression: Partial thickness burns, 18% TBSA, with possible inhalational
injury risk given enclosed-space exposure and voice hoarseness.

MANAGEMENT PLAN
IV Normal Saline per burns protocol (Parkland formula). Wounds covered
with cling film. IV Morphine 5mg given for analgesia. Burns unit referral
made.

DISPOSITION
Admit under burns unit; monitor airway closely given inhalational injury
risk.

FLAGS FOR DOCTOR
- Airway not yet definitively secured/assessed despite inhalational injury
  risk — close monitoring or early intubation discussion warranted.
- Tetanus status not mentioned.""",
    },
]


def main():
    total = 0
    for case in CASES:
        total = save_example(
            transcript=case["transcript"],
            additional_docs=case["additional_docs"],
            final_note=case["final_note"],
            deidentified_confirmed=True,
        )
        print(f"Seeded: {case['label']} (total examples now: {total})")
    print(f"\nDone. {total} total training examples in data/training_examples.jsonl")


if __name__ == "__main__":
    main()

"""
Enhanced seed script with comprehensive medical FAQ data.
Sources: Publicly available medical information (MedlinePlus, CDC, NHS style).
Usage: python scripts/seed_medical_data.py
"""

import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.services.pinecone_service import upsert_chunks
from app.api.ingest import chunk_text
from app.core.config import settings
import uuid

MEDICAL_DATA = [
    # ── Cardiovascular ────────────────────────────────────────────────────────
    {
        "source": "cardiovascular",
        "text": """Hypertension (high blood pressure) is a chronic condition where the force of blood against artery walls is consistently too high, typically defined as readings above 130/80 mmHg. It is often called the 'silent killer' because most people have no symptoms. Left untreated, hypertension can lead to heart attack, stroke, kidney failure, and vision loss. Risk factors include obesity, high sodium diet, physical inactivity, smoking, excessive alcohol, stress, and family history. Treatment includes lifestyle changes such as the DASH diet, regular exercise, limiting sodium to under 2300mg per day, reducing alcohol, and quitting smoking. Medications include ACE inhibitors, beta-blockers, calcium channel blockers, and diuretics."""
    },
    {
        "source": "cardiovascular",
        "text": """Heart disease is the leading cause of death worldwide. Coronary artery disease (CAD) occurs when plaque builds up in the arteries supplying the heart, reducing blood flow. Symptoms include chest pain (angina), shortness of breath, and fatigue. A heart attack (myocardial infarction) occurs when blood flow to part of the heart is completely blocked. Warning signs include chest pressure, pain radiating to the arm or jaw, sweating, nausea, and shortness of breath. Call emergency services immediately if a heart attack is suspected. Risk factors include high cholesterol, hypertension, diabetes, smoking, obesity, and family history. Prevention includes regular exercise, healthy diet, not smoking, and managing blood pressure and cholesterol."""
    },
    {
        "source": "cardiovascular",
        "text": """Cholesterol is a fatty substance in the blood. LDL (low-density lipoprotein) is 'bad' cholesterol that builds up in artery walls. HDL (high-density lipoprotein) is 'good' cholesterol that helps remove LDL. Total cholesterol above 200 mg/dL is borderline high; above 240 mg/dL is high. LDL above 130 mg/dL is concerning. High cholesterol has no symptoms but significantly increases risk of heart disease and stroke. Treatment includes dietary changes (reducing saturated and trans fats), exercise, weight loss, and medications called statins such as atorvastatin and simvastatin. Foods that help lower cholesterol include oats, nuts, olive oil, and fatty fish."""
    },
    {
        "source": "cardiovascular",
        "text": """Atrial fibrillation (AFib) is an irregular and often rapid heart rate that can increase the risk of stroke, heart failure, and other heart-related complications. Symptoms include palpitations, shortness of breath, weakness, fatigue, dizziness, and chest pain. AFib is diagnosed with an electrocardiogram (ECG). Treatment options include medications to control heart rate (beta-blockers, calcium channel blockers), blood thinners (anticoagulants like warfarin or apixaban) to prevent stroke, cardioversion to restore normal rhythm, and ablation procedures. AFib can be triggered by alcohol, caffeine, stress, sleep apnea, and thyroid problems."""
    },

    # ── Diabetes ──────────────────────────────────────────────────────────────
    {
        "source": "diabetes",
        "text": """Type 2 diabetes is a chronic condition where the body becomes resistant to insulin or does not produce enough insulin to maintain normal blood glucose levels. It accounts for 90-95% of all diabetes cases. Symptoms include frequent urination, excessive thirst, unexplained weight loss, fatigue, blurred vision, slow-healing wounds, and frequent infections. Diagnosis is confirmed with a fasting blood glucose above 126 mg/dL or HbA1c above 6.5%. Management includes healthy eating, regular physical activity, blood sugar monitoring, and medications such as metformin, SGLT2 inhibitors, and GLP-1 receptor agonists. Untreated diabetes can lead to neuropathy, nephropathy, retinopathy, and cardiovascular disease."""
    },
    {
        "source": "diabetes",
        "text": """Type 1 diabetes is an autoimmune condition where the immune system attacks insulin-producing beta cells in the pancreas, resulting in little or no insulin production. It can develop at any age but is most common in children and young adults. Symptoms appear suddenly and include extreme thirst, frequent urination, unintended weight loss, fatigue, blurred vision, and fruity-smelling breath. Type 1 diabetes requires lifelong insulin therapy. Modern management includes continuous glucose monitors (CGM), insulin pumps, and multiple daily injections. Carbohydrate counting is essential for dosing insulin correctly. Unlike Type 2, Type 1 cannot be prevented or reversed with lifestyle changes."""
    },
    {
        "source": "diabetes",
        "text": """Prediabetes is a condition where blood sugar levels are higher than normal but not yet high enough to be diagnosed as Type 2 diabetes. Fasting glucose between 100-125 mg/dL or HbA1c between 5.7-6.4% indicates prediabetes. Most people with prediabetes have no symptoms. Without intervention, prediabetes often progresses to Type 2 diabetes within 5 years. However, with lifestyle changes, progression can be prevented or delayed. The Diabetes Prevention Program showed that losing 5-7% of body weight and getting 150 minutes of moderate exercise per week reduced diabetes risk by 58%. Foods to limit include sugary drinks, white bread, white rice, and processed snacks."""
    },
    {
        "source": "diabetes",
        "text": """Hypoglycemia (low blood sugar) occurs when blood glucose falls below 70 mg/dL. It is most common in people with diabetes taking insulin or certain oral medications. Symptoms include shakiness, sweating, confusion, rapid heartbeat, hunger, dizziness, and in severe cases, loss of consciousness. The 15-15 rule: consume 15 grams of fast-acting carbohydrates (glucose tablets, juice, regular soda), wait 15 minutes, then recheck blood sugar. Repeat if still low. If unconscious, do not give food or drink; call emergency services. Causes include skipping meals, too much insulin, excessive exercise, and alcohol consumption."""
    },

    # ── Respiratory ───────────────────────────────────────────────────────────
    {
        "source": "respiratory",
        "text": """Asthma is a chronic inflammatory disease of the airways characterized by episodes of wheezing, breathlessness, chest tightness, and coughing, particularly at night or early morning. During an attack, the airways narrow, swell, and produce extra mucus. Triggers include allergens (pollen, dust mites, pet dander, mold), respiratory infections, exercise, cold air, air pollutants, and strong emotions. Asthma is managed with two types of inhalers: quick-relief (rescue) inhalers like albuterol for immediate symptoms, and long-term control inhalers containing corticosteroids like fluticasone. An asthma action plan helps patients recognize and respond to worsening symptoms. Asthma cannot be cured but can be well controlled."""
    },
    {
        "source": "respiratory",
        "text": """COPD (Chronic Obstructive Pulmonary Disease) is a chronic inflammatory lung disease that causes obstructed airflow. It includes emphysema and chronic bronchitis. The primary cause is long-term exposure to cigarette smoke; other causes include air pollution and occupational dust. Symptoms develop slowly and include chronic cough, mucus production, shortness of breath during activities, wheezing, and chest tightness. COPD is diagnosed with a spirometry test. It is not fully reversible but progression can be slowed by quitting smoking, using bronchodilators, inhaled steroids, pulmonary rehabilitation, and in severe cases, supplemental oxygen or surgery. COPD is the third leading cause of death worldwide."""
    },
    {
        "source": "respiratory",
        "text": """Pneumonia is an infection that inflames air sacs in one or both lungs, which may fill with fluid. Causes include bacteria (most commonly Streptococcus pneumoniae), viruses (including influenza and COVID-19), and fungi. Symptoms include cough with phlegm, fever, chills, and difficulty breathing. Severity ranges from mild ('walking pneumonia') to life-threatening. Bacterial pneumonia is treated with antibiotics. Viral pneumonia is managed with rest, fluids, and sometimes antiviral medications. High-risk groups include adults over 65, young children, smokers, and people with weakened immune systems or chronic conditions. Vaccines are available to prevent pneumococcal pneumonia and influenza-related pneumonia."""
    },
    {
        "source": "respiratory",
        "text": """The common cold is a viral infection of the nose and throat caused primarily by rhinoviruses. Symptoms include runny or stuffy nose, sore throat, cough, congestion, slight body aches, mild headache, sneezing, and low-grade fever. Symptoms typically appear 1-3 days after exposure and last 7-10 days. There is no cure for the common cold. Treatment is supportive: rest, staying hydrated, saline nasal sprays, and over-the-counter medications for symptom relief. Antibiotics do not work against viral infections. Prevention includes frequent handwashing, avoiding touching the face, and avoiding close contact with infected people. Adults average 2-3 colds per year."""
    },

    # ── Mental Health ─────────────────────────────────────────────────────────
    {
        "source": "mental_health",
        "text": """Depression (major depressive disorder) is a common and serious medical illness that negatively affects how you feel, think, and act. Symptoms must last at least two weeks and include persistent sad or empty mood, loss of interest in activities, changes in appetite and weight, sleep disturbances, fatigue, feelings of worthlessness or guilt, difficulty thinking or concentrating, and thoughts of death or suicide. Depression is caused by a combination of genetic, biological, environmental, and psychological factors. Treatments include psychotherapy (cognitive behavioral therapy), antidepressant medications (SSRIs, SNRIs), and for severe cases, electroconvulsive therapy. Depression is highly treatable; about 80-90% of people respond well to treatment."""
    },
    {
        "source": "mental_health",
        "text": """Anxiety disorders are the most common mental health conditions, affecting about 30% of adults at some point. Types include generalized anxiety disorder (GAD), panic disorder, social anxiety disorder, and specific phobias. GAD involves persistent, excessive worry about various aspects of life. Panic disorder involves recurrent unexpected panic attacks. Symptoms include excessive fear, restlessness, fatigue, difficulty concentrating, irritability, muscle tension, and sleep problems. Treatment includes psychotherapy (especially CBT), medications (SSRIs, SNRIs, benzodiazepines for short-term use), and lifestyle modifications including exercise, mindfulness, and stress management techniques. Untreated anxiety can significantly impair daily functioning."""
    },
    {
        "source": "mental_health",
        "text": """Sleep disorders affect millions of people and include insomnia, sleep apnea, restless legs syndrome, and narcolepsy. Insomnia involves difficulty falling or staying asleep. Sleep apnea causes breathing to stop repeatedly during sleep. Symptoms of sleep deprivation include daytime sleepiness, difficulty concentrating, mood changes, and impaired performance. Good sleep hygiene practices include maintaining a consistent sleep schedule, creating a dark and cool sleep environment, avoiding screens before bed, limiting caffeine after noon, and avoiding large meals close to bedtime. Adults need 7-9 hours of sleep per night. Chronic sleep deprivation increases risk of obesity, diabetes, cardiovascular disease, and mental health problems."""
    },

    # ── Infectious Disease ────────────────────────────────────────────────────
    {
        "source": "infectious_disease",
        "text": """Influenza (flu) is a contagious respiratory illness caused by influenza viruses. Symptoms come on suddenly and include fever, chills, muscle aches, cough, congestion, runny nose, headaches, and fatigue. Flu is different from a cold — symptoms are more severe and come on faster. Most people recover in 1-2 weeks, but serious complications including pneumonia can occur in high-risk groups. Annual flu vaccination is the best prevention, reducing risk by 40-60% in average years. Antiviral medications like oseltamivir (Tamiflu) work best when started within 48 hours of symptoms. High-risk groups include adults over 65, children under 5, pregnant women, and people with chronic conditions."""
    },
    {
        "source": "infectious_disease",
        "text": """COVID-19 is caused by the SARS-CoV-2 coronavirus. Symptoms range from mild to severe and include fever, cough, shortness of breath, fatigue, body aches, headache, loss of taste or smell, sore throat, congestion, nausea, and diarrhea. Symptoms appear 2-14 days after exposure. Most people recover at home with rest and fluids. Seek emergency care for trouble breathing, persistent chest pain, confusion, or bluish lips. Vaccination significantly reduces the risk of severe illness, hospitalization, and death. Long COVID involves symptoms lasting weeks or months after initial infection, including fatigue, brain fog, and shortness of breath. Prevention includes vaccination, wearing masks in high-risk settings, and good hand hygiene."""
    },
    {
        "source": "infectious_disease",
        "text": """Urinary tract infections (UTIs) are among the most common bacterial infections, particularly in women. They occur when bacteria, usually E. coli, enter the urinary tract. Symptoms include a burning sensation during urination, frequent urge to urinate, cloudy or strong-smelling urine, pelvic pain, and low-grade fever. UTIs are treated with antibiotics, typically trimethoprim-sulfamethoxazole or nitrofurantoin for simple cases. Drinking plenty of water helps flush bacteria. Cranberry products may help prevent recurrent UTIs. Risk factors include female anatomy, sexual activity, certain contraceptives, menopause, and urinary tract abnormalities. Untreated UTIs can spread to the kidneys (pyelonephritis), a more serious infection."""
    },

    # ── Musculoskeletal ───────────────────────────────────────────────────────
    {
        "source": "musculoskeletal",
        "text": """Arthritis refers to joint inflammation and includes over 100 different types. Osteoarthritis (OA) is the most common, caused by wear and tear of cartilage. Rheumatoid arthritis (RA) is an autoimmune disease where the immune system attacks joint lining. Symptoms include joint pain, stiffness, swelling, and reduced range of motion. OA commonly affects knees, hips, hands, and spine. RA affects joints symmetrically and can damage organs. Treatment for OA includes weight loss, exercise, physical therapy, pain relievers, and joint replacement surgery. RA is treated with disease-modifying antirheumatic drugs (DMARDs) and biologics. Regular low-impact exercise like swimming and cycling helps maintain joint function."""
    },
    {
        "source": "musculoskeletal",
        "text": """Lower back pain affects about 80% of adults at some point and is a leading cause of disability. Causes include muscle or ligament strain, bulging or ruptured disks, arthritis, osteoporosis, and poor posture. Most acute back pain improves within a few weeks with self-care. Red flags that require immediate attention include pain following trauma, pain with fever, pain with bowel or bladder problems, and pain radiating down the leg with numbness. Treatment includes over-the-counter pain relievers, heat or ice, staying active (bed rest is not recommended), physical therapy, and in some cases, steroid injections or surgery. Prevention includes regular exercise, maintaining healthy weight, proper lifting technique, and ergonomic workstations."""
    },

    # ── Nutrition & Preventive ────────────────────────────────────────────────
    {
        "source": "nutrition",
        "text": """A healthy diet is fundamental to preventing chronic disease. The Mediterranean diet, consistently ranked among the healthiest, emphasizes vegetables, fruits, whole grains, legumes, nuts, olive oil, and fish, with limited red meat and processed foods. The DASH diet (Dietary Approaches to Stop Hypertension) is specifically designed to lower blood pressure through reduced sodium and increased potassium, calcium, and magnesium. Processed and ultra-processed foods are linked to obesity, type 2 diabetes, heart disease, and cancer. Added sugars should be limited to less than 10% of daily calories. Dietary fiber from whole grains, vegetables, and legumes reduces cholesterol and improves gut health. Adults need at least 25-38 grams of fiber daily."""
    },
    {
        "source": "nutrition",
        "text": """Obesity is defined as a body mass index (BMI) of 30 or higher. It affects over 40% of US adults and is associated with type 2 diabetes, heart disease, stroke, certain cancers, sleep apnea, and osteoarthritis. Causes include excess calorie intake, physical inactivity, genetics, certain medications, and hormonal factors. Treatment combines dietary changes, increased physical activity, behavioral therapy, medications (orlistat, phentermine-topiramate, GLP-1 agonists like semaglutide), and bariatric surgery for severe cases. Even modest weight loss of 5-10% of body weight can significantly improve health outcomes. Sustainable weight loss involves gradual changes rather than extreme diets."""
    },
    {
        "source": "preventive",
        "text": """Preventive healthcare includes screenings, vaccinations, and lifestyle modifications to prevent disease. Key adult screenings include: blood pressure (every 1-2 years), cholesterol (every 4-6 years starting at 20), colorectal cancer (starting at 45), breast cancer mammography (starting at 40-50 depending on guidelines), cervical cancer Pap smear (every 3 years from age 21), diabetes screening (starting at 35 or earlier with risk factors), and lung cancer CT scan for heavy smokers aged 50-80. Essential adult vaccines include annual influenza, COVID-19 boosters, Tdap (tetanus, diphtheria, pertussis), shingles vaccine (Shingrix) at 50, and pneumococcal vaccine at 65."""
    },
    {
        "source": "preventive",
        "text": """Regular physical activity is one of the most important things adults can do for their health. The CDC recommends at least 150 minutes of moderate-intensity aerobic activity (brisk walking, cycling) or 75 minutes of vigorous activity per week, plus muscle-strengthening activities twice a week. Benefits include reduced risk of heart disease, stroke, type 2 diabetes, and certain cancers; improved mental health; stronger bones and muscles; and better sleep. Even short bouts of activity count — 10-minute walks add up. Sedentary behavior (prolonged sitting) increases health risks even in people who exercise regularly. Breaking up sitting time with brief movement every hour is beneficial."""
    },

    # ── Medications & Safety ──────────────────────────────────────────────────
    {
        "source": "medications",
        "text": """Over-the-counter pain relievers include acetaminophen (Tylenol) and NSAIDs like ibuprofen (Advil, Motrin) and naproxen (Aleve). Acetaminophen reduces pain and fever but does not reduce inflammation. It is safe for most people but can cause liver damage in high doses or with alcohol use; maximum adult dose is 4000mg per day (3000mg for older adults). NSAIDs reduce pain, fever, and inflammation but can cause stomach irritation, increase blood pressure, and affect kidney function. They should be avoided in people with kidney disease, peptic ulcers, or heart failure. Aspirin, also an NSAID, is used for pain and as a blood thinner to prevent heart attacks and strokes."""
    },
    {
        "source": "medications",
        "text": """Antibiotics are medications that kill or inhibit bacteria. They are only effective against bacterial infections, not viral ones like the common cold or flu. Common types include penicillins (amoxicillin), cephalosporins, macrolides (azithromycin), fluoroquinolones (ciprofloxacin), and tetracyclines (doxycycline). It is essential to complete the full course of antibiotics even if you feel better, to prevent antibiotic resistance. Side effects can include diarrhea, nausea, and allergic reactions. Antibiotic resistance is a major public health crisis caused by overuse and misuse of antibiotics. Some bacteria like MRSA are resistant to many antibiotics, making infections difficult to treat."""
    },

    # ── HIPAA & Healthcare Rights ─────────────────────────────────────────────
    {
        "source": "healthcare_policy",
        "text": """HIPAA (Health Insurance Portability and Accountability Act) is a US federal law that protects patient health information. The Privacy Rule gives patients rights over their health information and restricts who can access it. Protected Health Information (PHI) includes any information that can identify a patient, including name, address, birth date, Social Security number, and medical records. Patients have the right to access their own medical records, request corrections, and know who has accessed their information. Covered entities include healthcare providers, health plans, and healthcare clearinghouses. HIPAA violations can result in significant fines. The minimum necessary standard requires limiting PHI disclosure to the minimum needed to accomplish the purpose."""
    },
    {
        "source": "healthcare_policy",
        "text": """Patient rights in healthcare include the right to receive information about your condition, treatment options, and risks in understandable language; the right to make decisions about your care including the right to refuse treatment; the right to privacy and confidentiality; the right to emergency care regardless of ability to pay; the right to know the costs of treatment; and the right to file complaints. Informed consent means a healthcare provider must explain a procedure, its benefits, risks, and alternatives before you agree to it. Advance directives including living wills and healthcare proxies allow you to specify your wishes for medical care if you become unable to make decisions."""
    },
]


async def main():
    print(f"Seeding Pinecone with {len(MEDICAL_DATA)} medical knowledge entries...")
    print(f"Index: {settings.PINECONE_INDEX_NAME}")
    print()

    all_chunks = []
    for entry in MEDICAL_DATA:
        chunks = chunk_text(
            entry["text"],
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
        )
        for chunk in chunks:
            all_chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk,
                "metadata": {"source": entry["source"]},
            })

    print(f"Created {len(all_chunks)} chunks, uploading to Pinecone...")
    count = await upsert_chunks(all_chunks)
    print()
    print(f"✅ Successfully upserted {count} vectors to Pinecone!")
    print()
    print("Topics now available:")
    sources = list(set(e["source"] for e in MEDICAL_DATA))
    for s in sorted(sources):
        print(f"  • {s}")


if __name__ == "__main__":
    asyncio.run(main())

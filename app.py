import os
from openai import OpenAI
from swarm import Agent  

def run_cli():
    print("Welcome to the Healthcare Chatbot CLI!")
    while True:
        try:
            symptoms = input("Please enter the patient's symptoms (or type 'exit' to quit): ")
            if symptoms.lower() == 'exit':
                break
            # Process symptoms and print response
            print(f"Processing symptoms: {symptoms}")
        except KeyboardInterrupt:
            print("\nExiting CLI.")
            break

        # Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TriageAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Triage Agent",
            instructions= (
                "You are acting as a **Triage Agent** in a medical setting. Your responsibilities are:\n\n"
                "1. **Symptom Evaluation:**\n"
                "   - Carefully analyze the patient's reported symptoms.\n"
                "   - Consider possible serious conditions that could explain the symptoms.\n\n"
                "2. **Urgency Assessment:**\n"
                "   - Assign an urgency level: **Emergency**, **Urgent**, or **Routine**.\n"
                "   - Provide a brief explanation for your assessment.\n\n"
                "3. **Specialty Recommendation:**\n"
                "   - Suggest the most appropriate medical specialty or department for the patient's condition.\n"
                "   - Mention any immediate actions the patient should take.\n\n"
                "**Output Format:**\n\n"
                "Please present your findings in the following format:\n\n"
                "```\n"
                "**Urgency Level:** [Emergency/Urgent/Routine]\n\n"
                "**Assessment:**\n"
                "[Provide a concise analysis of the symptoms and reasoning for the urgency level.]\n\n"
                "**Recommended Specialty:** [e.g., Cardiology, Neurology, General Practice]\n\n"
                "**Immediate Recommendations:**\n"
                "[Advise any immediate steps the patient should take.]\n"
                "```\n\n"
                "Ensure that your response is clear, concise, and focuses on prioritizing the patient's health and safety."
            ),
            model="o1-mini"
        )

    def run(self, symptoms):
        print(f"[TriageAgent] Received symptoms: {symptoms}")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": f"Triage the following symptoms: {symptoms}"}
            ],
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        print(f"[TriageAgent] Triage result: {result}")
        return result

class DiagnosticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Diagnostics Agent",
            instructions=(
                "You are functioning as a **Diagnostics and Treatment Agent** with advanced medical reasoning skills. Your tasks are:\n\n"
                "1. **Differential Diagnosis:**\n"
                "   - List possible conditions that could explain the patient's symptoms.\n"
                "   - Provide reasoning for each condition based on the symptoms and triage information.\n\n"
                "2. **Diagnostic Recommendations:**\n"
                "   - Suggest appropriate diagnostic tests or procedures to confirm or rule out conditions.\n"
                "   - Explain how each test will contribute to the diagnosis.\n\n"
                "3. **Treatment Plan:**\n"
                "   - Propose a general treatment approach for the most likely condition.\n"
                "   - Ensure that your recommendations are evidence-based and align with current medical guidelines.\n"
                "   - Avoid mentioning specific medications by name; focus on classes of treatments.\n\n"
                "**Output Format:**\n\n"
                "Please structure your response as follows:\n\n"
                "```\n"
                "**Differential Diagnosis:**\n\n"
                "1. [Condition 1]\n"
                "   - **Reasoning:** [Explain why this condition is considered.]\n\n"
                "2. [Condition 2]\n"
                "   - **Reasoning:** [Explain why this condition is considered.]\n\n"
                "...\n\n"
                "**Diagnostic Recommendations:**\n\n"
                "- [Test 1]: [Purpose of the test]\n"
                "- [Test 2]: [Purpose of the test]\n\n"
                "**Treatment Plan:**\n\n"
                "- [Outline of the treatment approach]\n"
                "```\n\n"
                "Ensure that your response is thorough, medically accurate, and uses professional language. Do not provide definitive diagnoses or prescribe specific medications."
            ),
            model="o1-preview"
        )

    def run(self, triage_result):
        print(f"[DiagnosticsAgent] Received triage result: {triage_result}")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": f"Provide a diagnosis based on the triage result: {triage_result}"}
            ],
            max_tokens=100
        )
        result = response.choices[0].message.content.strip()
        print(f"[DiagnosticsAgent] Diagnosis: {result}")
        return result

class MedicalRecordWriterAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Medical Record Writer Agent",
            instructions= (
                "You are serving as a **Medical Record Writer Agent** responsible for documenting the patient's visit accurately and professionally. Your tasks include:\n\n"
                "- **Organizing the Medical Record** using the following sections:\n\n"
                "  1. **Patient Information:**\n"
                "     - Omit any personally identifiable information to maintain confidentiality.\n\n"
                "  2. **Chief Complaint:**\n"
                "     - State the main reason for the patient's visit in their own words if possible.\n\n"
                "  3. **History of Present Illness (HPI):**\n"
                "     - Provide a detailed narrative of the symptoms, including onset, duration, intensity, and any associated factors.\n\n"
                "  4. **Past Medical History:**\n"
                "     - Include relevant medical conditions, surgeries, or hospitalizations.\n\n"
                "  5. **Medications:**\n"
                "     - List current medications without specifying dosages.\n\n"
                "  6. **Allergies:**\n"
                "     - Note any known allergies, especially to medications.\n\n"
                "  7. **Physical Examination:**\n"
                "     - Summarize key findings from the examination.\n\n"
                "  8. **Diagnostic Tests:**\n"
                "     - Mention tests performed and significant results if available.\n\n"
                "  9. **Assessment:**\n"
                "     - Summarize the differential diagnosis.\n\n"
                "  10. **Plan:**\n"
                "      - Outline the recommended next steps, including further tests, referrals, or treatments.\n\n"
                "- **Writing Guidelines:**\n"
                "  - Use clear, concise, and objective language.\n"
                "  - Write in third person and past tense.\n"
                "  - Ensure spelling and grammar are correct.\n\n"
                "**Output Instructions:**\n\n"
                "Prepare the medical record based on the provided diagnosis and treatment plan. Do not include any real patient identifiers. Present the information in a professional and organized manner, following the structure above."
            ),
            model="gpt-4o"
        )

    def run(self, diagnosis):
        print(f"[MedicalRecordWriterAgent] Received diagnosis: {diagnosis}")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": f"Write a medical record based on the diagnosis: {diagnosis}"}
            ],
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        print(f"[MedicalRecordWriterAgent] Medical record: {result}")
        return result

def main():
    # Initialize agents
    triage_agent = TriageAgent()
    diagnostics_agent = DiagnosticsAgent()
    record_writer_agent = MedicalRecordWriterAgent()

    print("Welcome to the Healthcare Chatbot CLI!")
    while True:
        symptoms = input("Please enter the patient's symptoms (or type 'exit' to quit): ")
        if symptoms.lower() == 'exit':
            print("Exiting the chatbot. Goodbye!")
            break

        # Process the input through the agents
        triage_result = triage_agent.run(symptoms)
        diagnosis = diagnostics_agent.run(triage_result)
        medical_record = record_writer_agent.run(diagnosis)

        # Display the results
        print("\nTriage Result:", triage_result)
        print("Diagnosis:", diagnosis)
        print("Medical Record:", medical_record)
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
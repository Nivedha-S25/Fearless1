import streamlit as st
from ollama_nlp import analyze_soft_skills
from aptitude import get_question
from feedback import check_answer
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import whisper
import numpy as np
import av
import tempfile
import soundfile as sf
import random

st.set_page_config(page_title="Fearless | AI Interview & Aptitude Bot", layout="centered")

# ---------- GLOBAL CSS ---------- #
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://cdn.wallpapersafari.com/24/2/CgOJNk.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    .centered-title {
        text-align: center;
        color: #FF6F61;
        font-size: 60px;
        font-weight: bold;
    }
    .centered-subtitle {
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
        color: #ffffff;
    }
    .stButton>button {
        font-size: 18px;
        padding: 12px 30px;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

model = load_whisper()

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.frames.append(audio)
        return frame

    def get_audio(self):
        if self.frames:
            return np.concatenate(self.frames, axis=1).flatten()
        return None

# Page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    st.markdown("<div class='centered-title'>FEARLESS</div>", unsafe_allow_html=True)
    st.markdown("<div class='centered-subtitle'>Empowering your interview and aptitude preparation with AI.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Your Journey 🚀"):
            st.session_state.page = "main"
            st.rerun()

elif st.session_state.page == "main":
    st.title("🤖 AI Interview & Aptitude Bot using Ollama")
    mode = st.radio("Select Mode", ["Interview (Soft Skill)", "Aptitude Test"])

    if mode == "Interview (Soft Skill)":
        domain_data = {
       "Data Science": [
        ["How would you explain a complex model to a non-technical stakeholder?",
         "I'd use relatable analogies and visualizations, avoiding jargon, and focus on the business value the model provides."],
        ["What techniques do you use for feature selection?",
         "I use correlation analysis, recursive feature elimination, and tree-based models to assess feature importance."],
        ["How do you handle imbalanced datasets?",
         "I use techniques like SMOTE, under/oversampling, or adjusting class weights during training."]
    ],
    "Software Development": [
        ["Describe a time you had to fix a critical bug under pressure.",
         "I remained calm, quickly reproduced the issue, applied a hotfix, and documented the root cause for future prevention."],
        ["How do you ensure code quality in a team environment?",
         "Using code reviews, automated testing, and CI/CD pipelines to maintain standards and detect issues early."],
        ["What's your approach to version control?",
         "I follow GitFlow branching strategy and ensure all commits are documented with meaningful messages."]
    ],
    "Cybersecurity": [
        ["How do you prioritize security in a fast-paced dev environment?",
         "By integrating security into the SDLC with automated checks, code reviews, and continuous awareness training."],
        ["What’s your process for incident response?",
         "Identify, contain, eradicate, recover, and learn from the incident using a predefined response plan."],
        ["How do you secure an API?",
         "With authentication, authorization, rate limiting, and input validation using tools like OAuth and API gateways."]
    ],
    "Cloud Computing": [
        ["How do you handle data privacy in cloud deployments?",
         "Through encryption, access controls, compliance checks, and choosing reputable cloud providers with strong SLAs."],
        ["How do you monitor cloud infrastructure?",
         "Using tools like AWS CloudWatch, Azure Monitor, and Prometheus to track metrics, logs, and alerts."],
        ["What are key strategies for cloud cost optimization?",
         "Rightsizing instances, reserved instances, autoscaling, and continuous cost monitoring."]
    ],
    "AI & ML": [
        ["How do you ensure fairness in AI model predictions?",
         "By using balanced datasets, bias detection tools, and regular auditing across different demographic groups."],
        ["How do you prevent overfitting?",
         "Using regularization, cross-validation, early stopping, and dropout techniques."],
        ["Explain the difference between bagging and boosting.",
         "Bagging reduces variance using parallel learners, boosting reduces bias using sequential learners."]
    ],
    "Web Development": [
        ["Describe how you handle cross-browser compatibility issues.",
         "I use CSS resets, test with tools like BrowserStack, and adhere to web standards for consistent behavior."],
        ["How do you improve website performance?",
         "Minifying code, lazy loading, optimizing images, and using CDN."],
        ["What is responsive design and how do you implement it?",
         "Using media queries, flexible grids, and relative units to adapt to different screen sizes."]
    ],
    "Mobile App Dev": [
        ["How do you test your app for various screen sizes and OS versions?",
         "Using responsive design principles, emulators, and real devices during QA."],
        ["How do you manage state in mobile apps?",
         "Using providers like Redux, Bloc, or MobX depending on the platform and scale."],
        ["Explain your strategy for app performance optimization.",
         "Profiling, minimizing re-renders, reducing dependencies, and async loading of data."]
    ],
    "UI/UX Design": [
        ["How do you gather and implement user feedback?",
         "By conducting usability tests, collecting feedback, prioritizing insights, and iterating designs."],
        ["How do you handle design handoff to developers?",
         "Using design systems and tools like Figma/Zeplin with clear annotations."],
        ["What's the role of accessibility in your design process?",
         "I use contrast checkers, alt text, semantic HTML, and keyboard navigation for inclusivity."]
    ],
    "Product Management": [
        ["How do you handle conflicts between business and engineering teams?",
         "I facilitate discussions to align goals, clarify requirements, and find win-win solutions."],
        ["How do you prioritize features in a roadmap?",
         "Using frameworks like MoSCoW, RICE, or Kano Model based on business impact and effort."],
        ["How do you define product success?",
         "By tracking KPIs such as adoption rate, churn, customer satisfaction, and revenue impact."]
    ],
    "Business Analysis": [
        ["Tell me how you capture and communicate business requirements.",
         "Via stakeholder interviews, use cases, diagrams, and user stories documented clearly."],
        ["How do you handle scope creep?",
         "By managing expectations, documenting changes, and ensuring they align with business goals."],
        ["How do you validate a requirement?",
         "By verifying alignment with business goals, user needs, and technical feasibility."]
    ],
    "DevOps": [
        ["Describe your experience with CI/CD pipelines.",
         "I set up CI/CD using Jenkins and GitHub Actions, ensuring quick feedback and rollback mechanisms."],
        ["How do you ensure zero-downtime deployment?",
         "Using blue-green or canary deployments with proper monitoring."],
        ["What tools do you use for infrastructure as code?",
         "Terraform, Ansible, and AWS CloudFormation depending on the environment."]
    ],
    "Database Admin": [
        ["How do you ensure database security and availability?",
         "With access controls, backups, monitoring, and replication across regions."],
        ["What’s your backup and recovery strategy?",
         "Regular full and incremental backups, with tested restore procedures."],
        ["How do you optimize slow queries?",
         "Using indexing, query analysis tools, and proper normalization."]
    ],
    "Game Dev": [
        ["How do you balance performance and visual quality in games?",
         "By profiling bottlenecks, using LODs, and optimizing shaders/textures."],
        ["How do you handle multiplayer synchronization?",
         "Using authoritative servers, lag compensation, and state interpolation."],
        ["What game engine do you prefer and why?",
         "Unity for flexibility and tooling, Unreal for visual fidelity and performance."]
    ],
    "Blockchain": [
        ["How do you explain blockchain to someone from a non-tech background?",
         "It’s like a public spreadsheet where everyone sees and verifies changes, and no one can tamper it alone."],
        ["What’s the difference between public and private blockchains?",
         "Public is open and decentralized; private is permissioned and controlled by an entity."],
        ["How do you handle scalability issues in blockchain?",
         "Layer-2 solutions, sharding, and consensus improvements like PoS."]
    ],
    "NLP": [
        ["What are common issues when working with multi-language NLP systems?",
         "Data imbalance, tokenization issues, and inconsistent translation quality across languages."],
        ["What preprocessing steps do you usually follow?",
         "Lowercasing, tokenization, stopword removal, lemmatization, and handling out-of-vocabulary tokens."],
        ["How do you evaluate NLP models?",
         "Using metrics like BLEU, ROUGE, perplexity, and human validation."]
    ],
    "IoT": [
        ["What are major security concerns with IoT devices?",
         "Weak authentication, lack of encryption, and insecure firmware updates."],
        ["How do you manage IoT device updates?",
         "Using OTA (Over-the-Air) updates with secure boot and rollback mechanisms."],
        ["Which protocols are commonly used in IoT?",
         "MQTT, CoAP, and HTTP depending on bandwidth, latency, and device capability."]
    ],
    "Robotics": [
        ["How do you troubleshoot sensor failures in robotic systems?",
         "Using diagnostics tools, logs, and fallbacks like sensor fusion."],
        ["What is inverse kinematics?",
         "A method to calculate joint angles needed to reach a specific position with an end-effector."],
        ["How do robots localize themselves?",
         "Using techniques like SLAM, GPS, and dead reckoning depending on environment."]
    ],
    "Networking": [
        ["How would you diagnose intermittent network issues?",
         "Using packet sniffers like Wireshark and logs to identify patterns."],
        ["What's the difference between TCP and UDP?",
         "TCP is connection-oriented and reliable; UDP is faster but connectionless and less reliable."],
        ["How do you secure a network?",
         "Firewalls, intrusion detection systems, VPNs, and regular patching."]
    ],
    "IT Support": [
        ["How do you deal with an angry or frustrated user?",
         "I stay calm, listen actively, reassure them, and solve their issue empathetically."],
        ["What tools do you use for remote troubleshooting?",
         "TeamViewer, AnyDesk, and built-in OS tools like Remote Desktop or SSH."],
        ["How do you document and track issues?",
         "Using ticketing systems like Jira, ServiceNow, or Freshdesk."]
    ],
    "Testing / QA": [
        ["How do you decide what to automate in your tests?",
         "I automate repetitive, stable, and high ROI tests like regression suites."],
        ["What's the difference between black-box and white-box testing?",
         "Black-box tests behavior without internal knowledge; white-box uses code structure."],
        ["How do you handle flaky tests?",
         "By isolating causes, improving test stability, and running in clean environments."]
    ],
    "IT Consulting": [
        ["How do you approach giving strategic tech advice to a client?",
         "I analyze their goals, current stack, and present cost-effective options aligned to growth."],
        ["How do you manage change resistance?",
         "By involving stakeholders early, clear communication, and showing business benefits."],
        ["What’s your discovery phase like in a new project?",
         "I assess current systems, interview key users, and define success metrics."]
    ],
    "Technical Writing": [
        ["How do you simplify complex technical content?",
         "Using clear language, examples, diagrams, and structuring content for clarity."],
        ["What tools do you use for documentation?",
         "Markdown, Sphinx, Docusaurus, and tools like Notion or Confluence."],
        ["How do you write for different audiences?",
         "I adapt tone, depth, and terminology based on technical proficiency and goals."]
    ]
} 

        domain = st.selectbox("Select Your Domain", list(domain_data.keys()))
        selected_qa = random.choice(domain_data[domain])
        question, preferred_answer = selected_qa

        st.write("🧠 Domain-Specific Question:")
        st.info(question)

        st.markdown("### 🎤 Record Your Answer")
        ctx = webrtc_streamer(
            key="speech",
            audio_receiver_size=1024,
            sendback_audio=False,
            audio_processor_factory=AudioProcessor
        )

        if ctx.audio_processor and ctx.state.playing:
            audio_data = ctx.audio_processor.get_audio()
            if audio_data is not None and len(audio_data) > 16000 * 3:  # at least 3 sec
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                    sf.write(tmpfile.name, audio_data, samplerate=16000)
                    result = model.transcribe(tmpfile.name)
                    st.session_state.transcribed_text = result['text']
                    st.success("✅ Transcription Complete!")

        user_input = st.text_area("Analyze:", st.session_state.get("transcribed_text", ""))

        if st.button("Analyze"):
            if user_input.strip():
                with st.spinner("Analyzing..."):
                    try:
                        result = analyze_soft_skills(user_input)
                        if result and isinstance(result, str) and result.strip():
                            st.success("Analysis Complete:")
                            st.markdown(result)
                        else:
                            st.error("processing")
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                st.markdown("**Preferred/Ideal Answer:**")
                st.info(preferred_answer)
            else:
                st.warning("Please transcribe or paste your response.")

    elif mode == "Aptitude Test":
        if "question" not in st.session_state:
            st.session_state.question, st.session_state.correct = get_question()
            st.session_state.answered = False
            st.session_state.feedback = ""

        st.write("🧪 Question:", st.session_state.question)
        user_ans = st.text_input("Your Answer:")

        if st.button("Check") and not st.session_state.answered:
            st.session_state.feedback = check_answer(user_ans, st.session_state.correct)
            st.session_state.answered = True

        if st.session_state.answered:
            st.write(st.session_state.feedback)
            if st.button("Next Question"):
                st.session_state.question, st.session_state.correct = get_question()
                st.session_state.answered = False
                st.session_state.feedback = ""

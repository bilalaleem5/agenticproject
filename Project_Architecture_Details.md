# LaunchMind: Technical Architecture & File Details

Yeh document aap ke Final Agentic AI Project (LaunchMind) ki technical details aur file-by-file working ko explain karta hai. Yeh aap ko presentation aur viva mein bohut help karega.

---

## 1. Purana Workflow (Assignment 3) vs Naya Workflow (Final Project)

**Purana Workflow (Assignment 3):**
Assignment 3 ek "Linear Script" thi. Is mein system seedha chalta tha:
1. CEO ne task liya.
2. Product agent ko pass kiya.
3. Engineer ne code likh kar GitHub PR bana di.
4. Marketing ne email/slack bhej di.
*Koyi check and balance nahi tha, koyi memory nahi thi, aur koyi audit log nahi tha.*

**Naya Workflow (Final Project):**
Yeh ek proper **Autonomous Multi-Agent System (MAS)** hai:
1. **Shared Memory:** Ab sab agents ek central memory share karte hain.
2. **SQLite Message Bus:** Har aapas ki communication (kis ne kya message bheja) ek database mein save hoti hai (Audit Trail).
3. **Ethics Guardrail (QA):** Jo bhi kaam hota hai, akhir mein QA Agent usay check karta hai. Agar ethical score 7.0 se kam ho, toh automatically wapas bhej diya jata hai theek karne ke liye (Feedback Loop).
4. **Empirical Benchmarking:** 5 scenarios pe auto-testing hoti hai aur data collect kiya jata hai.

---

## 2. File-by-File Details (Kon si file mein kya ho raha hai?)

### 🚀 Entry Points & Configuration
- **`mas_main.py` / `main.py`**: Yeh project ka starting point hai. Yeh user se "Startup Idea" mangta hai, Message Bus (database) ko initialize karta hai, aur phir CEO Agent ko start kar deta hai.
- **`config.py`**: Is file mein saari API keys (Gemini, GitHub, Slack) aur system settings load hoti hain taake security maintain rahay.

### 🧠 Core Agents (`agents/` folder)
- **`ceo_agent.py`**: Yeh system ka **"Orchestrator"** hai. Yeh kisi specific task ka code nahi likhta, balke doosre agents ko "TASK" assign karta hai aur un se "RESULT" leta hai. Agar QA Agent fail kar de, toh CEO baqi agents ko **revision request** (dobara kaam karne ka order) bhejta hai.
- **`product_agent.py`**: CEO isko idea bhejta hai. Yeh LLM ko use kar ke ek proper "Product Specification" (JSON format) banata hai jis mein user personas aur features hote hain.
- **`github_engineer_agent.py`**: Yeh product spec read karta hai, ek Landing Page (HTML) generate karta hai. Phir yeh **GitHub REST API** use kar ke khud naya branch banata hai, code commit karta hai, aur "Automated PR" open karta hai.
- **`slack_marketing_agent.py`**: Yeh Slack ki API use kar ke `#launches` channel mein proper formatted message (Block Kit) post karta hai. Yeh real email (SMTP) send karne ka logic bhi handle karta hai.

### 🛡️ The New "Final Project" Features (Advanced Files)
- **`qa_agent.py` (Ethics Guardrail)**: Yeh sab se important new file hai. PR aur Slack post ban'ne ke baad, CEO sab kuch QA Agent ko deta hai. QA usko 4 cheezon par check karta hai: Professional tone, no false claims, clarity, aur alignment. Yeh 0-10 ek Ethics Score deta hai. Agar score pass ho, toh hi system finish hota hai.
- **`message_bus.py`**: Yeh ek **SQLite Database** connection hai. Jab CEO Product ko task deta hai, ya QA result deta hai, har message is database table `messages` mein save ho jata hai. Yeh "Complex Computing" aur "Auditability" ke criteria ko meet karta hai.
- **`memory.py`**: Yeh ek "Shared Scratchpad" hai. Pehle agar Engineer ko Idea chahiye tha toh CEO ko lamba message bhejna parta tha. Ab Engineer direct `memory["idea"]` se data read kar leta hai (Context Window bachane ke liye).

### 📊 Research & Benchmarking
- **`evaluation_benchmark.py`**: Final project mein "Research & Experimentation" zaroori tha. Yeh script MAS ko 5 different dummy startup ideas par loop mein chalati hai. Phir yeh measure karti hai ke kitne seconds lagay (latency) aur kya ethics score aaya, aur `evaluation_results.json` file generate karti hai.
- **`paper.tex`**: Yeh aap ki 6-page ki complete IEEE research paper hai. Is mein system ka architecture, related work (AutoGPT etc se comparison), aur evaluation benchmark ke results shamil hain.

---

## 3. Data Flow (System Kese Kaam Karta Hai?)

Ek typical run is tarah execute hota hai:

1. **User Input:** `mas_main.py` chalta hai, user idea deta hai (e.g., "AI Sales Bot").
2. **CEO $\rightarrow$ Product:** CEO Product ko "TASK" message bhejta hai.
3. **Product $\rightarrow$ CEO:** Product JSON spec banata hai, Shared Memory mein save karta hai, aur CEO ko "RESULT" bhejta hai.
4. **CEO $\rightarrow$ Engineer & Marketing:** CEO parallel/sequential in dono ko spec pakrata hai.
5. **Engineer Action:** GitHub PR ban jati hai.
6. **Marketing Action:** Slack post draft ho jati hai.
7. **CEO $\rightarrow$ QA:** CEO in dono ki final output QA ko deta hai.
8. **QA Action:** QA Ethics score calculate karta hai (e.g., 9/10).
9. **CEO Finalize:** QA pass kare toh Slack pe message live ho jata hai aur system success return karta hai. (Agar QA fail kare toh loop wapas step 4 pe jata hai).

---

## 💡 Viva / Presentation Tips
Agar sir poochein ke "Assignment 3 mein bhi toh GitHub aur Slack tha, is mein naya kya hai?", toh aap ne yeh 3 points bolne hain:

1. *"Sir, pichlay assignment mein workflow linear tha. Is mein maine **Autonomous Feedback Loop** add kiya hai QA Agent ke through. System ab khud errors identify kar ke khud ko fix karta hai bina human intervention ke."*
2. *"Sir, is mein maine **Persistent SQLite Message Bus** implement ki hai. Har agent ka decision auditable hai aur database mein save hota hai, jo enterprise MAS systems ka core requirement hota hai."*
3. *"Sir, assignment 3 sirf ek script thi. Is project mein maine **Empirical Evaluation** ki hai 5 scenarios pe, aur us ki base par ek proper IEEE Research Paper tayyar kiya hai."*

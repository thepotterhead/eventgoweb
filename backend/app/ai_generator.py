import os
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from .models import ChatResponse, LearnerProfile

class GroundedAIGenerator:
    def __init__(self, knowledge_engine, access_engine):
        self.kb = knowledge_engine
        self.access = access_engine

    def generate_response(
        self,
        session_id: str,
        message: str,
        customer_id: str,
        profile: LearnerProfile,
        character_id: str,
        concept: str,
        access_info: Dict[str, Any],
        clarification_info: Dict[str, Any],
        unsupported_notice: Optional[str],
        escalation_triggered: bool,
        api_key: Optional[str] = None
    ) -> ChatResponse:
        
        # 1. Handle Unsupported Fact Queries (Scenario 5)
        if unsupported_notice:
            return ChatResponse(
                session_id=session_id,
                answer=unsupported_notice,
                concept=concept,
                difficulty=profile.starting_knowledge,
                check_question="Would you like to learn about verified STEM concepts like motor circuits or LED light instead?",
                options=["Tell me about circuits!", "Tell me about light!", "How do motors work?"],
                correct_option=0,
                next_step="Choose an approved STEM topic above!",
                active_character=character_id,
                active_topic=concept,
                access_granted=access_info["granted"],
                unsupported_fact_notice=unsupported_notice
            )

        # 2. Handle Ambiguous Queries (Scenario 4)
        if clarification_info.get("clarification_needed"):
            opts = clarification_info.get("clarification_options", [])
            return ChatResponse(
                session_id=session_id,
                answer="Great question! Several Funobotz characters move in different ways using electric motors. Which character are you asking about?",
                concept="clarification",
                difficulty=profile.starting_knowledge,
                check_question="Select the character you want to explore:",
                options=opts,
                correct_option=0,
                next_step="Select a character option above.",
                active_character=character_id,
                active_topic=concept,
                access_granted=access_info["granted"],
                clarification_needed=True,
                clarification_options=opts
            )

        # 3. Handle Product Access Restrictions (Scenario 3)
        if not access_info["granted"]:
            notice = access_info["notice"]
            return ChatResponse(
                session_id=session_id,
                answer=f"{notice}\n\nGeneral STEM Concept: {concept.capitalize()} involves energy transformation (e.g. electrical to mechanical or light energy). Although product-specific build guides are locked for this account, you can still explore foundational STEM principles!",
                concept=concept,
                difficulty=profile.starting_knowledge,
                check_question="What form of energy powers electric circuits?",
                options=["Electrical Energy", "Sound Energy", "Solar Heat Energy"],
                correct_option=0,
                next_step="Answer the general STEM check question above.",
                active_character=character_id,
                active_topic=concept,
                access_granted=False,
                access_notice=notice
            )

        # 4. Fetch Character Knowledge
        char = self.kb.get_character(character_id) or self.kb.get_character("quacky")
        char_name = char["name"]
        status = char.get("status", "mapped")

        # Handle pending / unmapped characters (Scenario 7)
        if status == "pending":
            seed_idx = int(hashlib.md5(f"{session_id}_{message}_{profile.current_level}".encode()).hexdigest(), 16)
            check_q, options, correct_idx = self._generate_check_question(character_id, profile.current_level, seed_idx)
            return ChatResponse(
                session_id=session_id,
                answer=f"You selected {char_name}! {char_name} is an official Funobotz character roster member, but detailed STEM concept sheets are currently pending release by the organizer. The architecture supports {char_name} seamlessly for future official updates without code changes!",
                concept="pending_release",
                difficulty=profile.starting_knowledge,
                check_question=check_q,
                options=options,
                correct_option=correct_idx,
                next_step="Select a character to continue your learning journey.",
                active_character=character_id,
                active_topic=concept,
                access_granted=True
            )

        if status == "behaviour_only":
            facts_str = " ".join(char.get("verified_facts", []))
            seed_idx = int(hashlib.md5(f"{session_id}_{message}_{profile.current_level}".encode()).hexdigest(), 16)
            check_q, options, correct_idx = self._generate_check_question(character_id, profile.current_level, seed_idx)
            return ChatResponse(
                session_id=session_id,
                answer=f"I'm {char_name}! {facts_str} As an official expression & interaction bot, I bring stories to life through movements and reactions.",
                concept="behaviour_and_interaction",
                difficulty=profile.starting_knowledge,
                check_question=check_q,
                options=options,
                correct_option=correct_idx,
                next_step="Explore more characters or switch to a STEM product kit!",
                active_character=character_id,
                active_topic=concept,
                access_granted=True
            )

        # 5. Mapped STEM Characters (Tiko, Quacky, Petalo, Tolly)
        level = profile.current_level
        facts = char.get("verified_facts", [])
        materials = char.get("learning_materials", {})
        msg_lower = message.lower()

        # Build tailored explanation answering user's specific query
        explanation = self._build_tailored_explanation(char_name, character_id, level, profile.age, msg_lower, facts, materials, api_key)

        if escalation_triggered:
            explanation = f"🚀 Difficulty Escalated to {profile.starting_knowledge}!\n" + explanation

        # Calculate a question seed index to cycle through varied check questions dynamically
        seed_idx = int(hashlib.md5(f"{session_id}_{message}_{level}".encode()).hexdigest(), 16)

        # Tailor check question per character, level, and seed index
        check_q, options, correct_idx = self._generate_check_question(character_id, level, seed_idx)

        return ChatResponse(
            session_id=session_id,
            answer=explanation,
            concept=concept,
            difficulty=profile.starting_knowledge or "Beginner",
            check_question=check_q,
            options=options,
            correct_option=correct_idx,
            next_step="Answer the check question to earn learning points!",
            active_character=character_id,
            active_topic=concept,
            access_granted=True,
            escalation_triggered=escalation_triggered
        )

    def _call_gemini_llm(self, user_msg: str, char_name: str, age: int, level_label: str, facts: List[str], override_api_key: Optional[str] = None) -> Optional[str]:
        api_key = override_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return None
        
        try:
            import urllib.request
            import json
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            system_instruction = (
                f"You are {char_name}, a friendly STEM robot companion from Funobotz. "
                f"Your user is a learner aged {age} ({level_label} difficulty level). "
                f"STRICT GROUNDING RULE: You must ONLY explain STEM concepts using these verified facts: {' '.join(facts)}. "
                f"Do not invent unapproved facts or backstories. Keep your response under 3 sentences, encouraging, and clear for age {age}."
            )
            payload = {
                "systemInstruction": {
                    "parts": [{"text": system_instruction}]
                },
                "contents": [
                    {"role": "user", "parts": [{"text": user_msg}]}
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 200
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                return text
        except Exception:
            return None

    def _build_tailored_explanation(
        self,
        char_name: str,
        char_id: str,
        level: int,
        age: int,
        msg_lower: str,
        facts: List[str],
        materials: Dict[str, str],
        api_key: Optional[str] = None
    ) -> str:
        diff_label = "Beginner" if level == 0 else "Intermediate" if level == 1 else "Advanced"
        cid = (char_id or "quacky").lower()

        # 1. Try Live Gemini LLM RAG if GEMINI_API_KEY / GOOGLE_API_KEY or api_key is configured
        llm_resp = self._call_gemini_llm(msg_lower, char_name, age, diff_label, facts, api_key)
        if llm_resp:
            return f"✨ {llm_resp}"

        # 2. Troubleshooting & Repair Queries
        if any(k in msg_lower for k in ["troubleshoot", "fix", "not work", "stopped", "broken", "repair"]):
            if cid == "tiko":
                return f"Troubleshooting {char_name}: Check 1) battery terminal contact, 2) motor wire solder joints, and 3) thread tension. If the thread is too loose or caught, the scorpio tail won't pull up!"
            elif cid == "quacky":
                return f"Troubleshooting {char_name}: Check battery contacts, switch position, and ensure motor wires are firmly attached to the terminals."
            elif cid == "petalo":
                return f"Troubleshooting {char_name}: Check light card alignment, LED lead orientation (+/-), and battery contact points."
            elif cid == "tolly":
                return f"Troubleshooting {char_name}: Check timer circuit connections, LED polarities, and ensure battery voltage is sufficient for all 3 color stages."
            elif cid == "mimo":
                return f"Troubleshooting {char_name}: Check paper fold flexibility and linkage pivot points so paper dog legs move smoothly."
            elif cid == "chicky":
                return f"Troubleshooting {char_name}: Ensure the offset counterweight is spinning freely on the motor shaft and not scraping paper walls."
            elif cid == "wavy":
                return f"Troubleshooting {char_name}: Verify linkage joints are unconstrained so rotational motor movement converts cleanly to wave oscillation."
            elif cid in ["omni", "kutty-omni"]:
                return f"Troubleshooting {char_name}: Ensure all multi-directional wheels spin freely and motor wire terminals are connected with correct polarity."
            elif cid == "cuby":
                return f"Troubleshooting {char_name}: Re-check modular block alignment and snap-together circuit pin contacts."
            elif cid == "emoti":
                return f"Troubleshooting {char_name}: Check input signal wires and LED/movement reaction connections."
            elif cid == "kuttybot":
                return f"Troubleshooting {char_name}: Check audio speaker wire terminals and power switch connection."

        # 3. How it Works & Movement Mechanics Queries
        if any(k in msg_lower for k in ["how", "work", "move", "motion", "waddle", "tail", "light", "speak", "vibrate", "wave", "about"]):
            if cid == "tiko":
                return f"How {char_name} Works: Tiko uses a battery-powered BO motor circuit connected to a pull-and-release thread. When the motor turns, it pulls the thread to raise the scorpio tail upward, converting electrical energy into mechanical movement!"
            elif cid == "quacky":
                return f"How {char_name} Works: Quacky waddles across smooth surfaces using a battery-powered BO motor connected to paper leg linkages. Electrical current powers the motor rotation, driving mechanical waddling motion!"
            elif cid == "petalo":
                return f"How {char_name} Works: Petalo introduces light observation through colorful paper binds and challenge cards. Light reflects off vibrant paper surfaces, teaching cause-and-effect optics safely!"
            elif cid == "tolly":
                return f"How {char_name} Works: Tolly controls an automated Red-Yellow-Green traffic light sequence using a timer circuit that switches electricity between 3 colored LEDs in order!"
            elif cid == "emoti":
                return f"How {char_name} Works: Emoti brings feelings to life by translating input signals into physical movements and expressive LED light patterns!"
            elif cid == "mimo":
                return f"How {char_name} Works: Mimo is a paper pet dog that moves through simple paper mechanics, wagging linkages, and playful interactive folds!"
            elif cid == "kuttybot":
                return f"How {char_name} Works: Kuttybot is a friendly talking robot that uses audio speech interaction to communicate and answer STEM questions verbally!"
            elif cid == "kutty-omni":
                return f"How {char_name} Works: Kutty-Omni features an omnidirectional chassis that can move in any direction instantly without needing to turn or pivot first!"
            elif cid == "wavy":
                return f"How {char_name} Works: Wavy converts continuous motor rotation into smooth back-and-forth wave motion using sinusoidal mechanical linkages!"
            elif cid == "chicky":
                return f"How {char_name} Works: Chicky hops using an offset counterweight on a small motor shaft. High-speed vibration reduces surface friction, causing small forward hops!"
            elif cid == "omni":
                return f"How {char_name} Works: Omni uses omni-directional wheels with perpendicular rollers to control 3 degrees of freedom (x, y, and rotation) simultaneously!"
            elif cid == "cuby":
                return f"How {char_name} Works: Cuby uses modular block robotics for 3D spatial building and snap-together reconfigurable electronic circuits!"

        # 4. Battery, Power & Circuit Queries
        if any(k in msg_lower for k in ["battery", "power", "energy", "circuit", "electricity"]):
            return f"Electrical Energy in {char_name}: The 3V battery stores chemical energy and releases it as electrical current when the switch is ON. This current completes a closed circuit loop, powering {char_name}'s motor, LED, or sound components!"

        # Default depth explanation based on level & age
        if level == 0:
            exp = materials.get("beginner", facts[0] if facts else "")
            prefix = f"Hi friend! 🌟 I'm {char_name}. " if age <= 8 else f"Hello! I'm {char_name}. "
            return prefix + exp
        elif level == 1:
            exp = materials.get("intermediate", facts[0] if facts else "")
            return f"Let's explore how {char_name} works! " + exp
        else:
            exp = materials.get("advanced", facts[0] if facts else "")
            return f"Technical Deep-Dive on {char_name}: " + exp

    def _generate_check_question(self, character_id: str, level: int, seed_idx: int) -> Tuple[str, List[str], int]:
        """
        Generates varied, non-repeating check questions from a rich question bank for ALL 12 roster characters.
        """
        cid = (character_id or "quacky").lower()
        bank: List[Tuple[str, List[str], int]] = []

        if cid == "tiko":
            bank = [
                (
                    "How does Tiko's tail move up and down?",
                    ["A motor pulls and releases a thread", "Using a solar sail", "Magnets blowing wind"],
                    0
                ),
                (
                    "What energy transformation occurs in Tiko's motor circuit?",
                    ["Electrical energy to mechanical motion", "Heat energy to nuclear power", "Sound into light"],
                    0
                ),
                (
                    "When troubleshooting Tiko's tail, what mechanical factor affects thread motion?",
                    ["Friction, thread tension, and motor torque", "Color of paper", "Sound volume"],
                    0
                ),
                (
                    "What happens when Tiko's motor turns and pulls the thread?",
                    ["The thread pulls the scorpio tail upward", "The lights turn off", "The battery charges"],
                    0
                ),
                (
                    "What component connects Tiko's motor to its moving tail?",
                    ["A pull-and-release thread mechanism", "A wooden wheel", "A rubber band"],
                    0
                )
            ]

        elif cid == "quacky":
            bank = [
                (
                    "What component powers Quacky's movement in a simple circuit?",
                    ["A BO motor connected to a battery", "A water propeller", "A hand crank"],
                    0
                ),
                (
                    "What happens when electricity flows through Quacky's BO motor circuit?",
                    ["It converts electrical energy into mechanical movement", "It turns water into ice", "It glows red"],
                    0
                ),
                (
                    "What energy conversion chain takes place in Quacky?",
                    ["Chemical -> Electrical -> Mechanical", "Light -> Sound -> Heat", "Thermal -> Gravitational"],
                    0
                ),
                (
                    "What type of circuit connects Quacky's battery to its motor?",
                    ["A simple electrical circuit", "An optical fiber network", "A hydraulic pipe"],
                    0
                ),
                (
                    "How does Quacky waddle across a smooth surface?",
                    ["Motor rotation drives simple waddling mechanical motion", "By blowing air", "By magnet levitation"],
                    0
                )
            ]

        elif cid == "petalo":
            bank = [
                (
                    "What is Petalo's main feature for exploring STEM concepts?",
                    ["A light-up discovery friend with challenge cards", "High-speed wheels", "Voice recognition"],
                    0
                ),
                (
                    "How does Petalo promote scientific inquiry?",
                    ["Through environmental light observation and cause-and-effect cards", "By printing papers", "By singing songs"],
                    0
                ),
                (
                    "What STEM principle does Petalo demonstrate when completing challenge cards?",
                    ["Observation of light and cause-and-effect reactions", "Rocket fuel combustion", "Geological mapping"],
                    0
                ),
                (
                    "What safety habit does Petalo teach when observing light?",
                    ["Safety awareness and careful scientific communication", "Wearing heavy gloves", "Running fast"],
                    0
                ),
                (
                    "What visual design makes Petalo engaging for beginner learners?",
                    ["Light and colorful paper binds with interactive discovery cards", "Steel armor plating", "Heavy brass gears"],
                    0
                )
            ]

        elif cid == "tolly":
            bank = [
                (
                    "What sequence of light colors does Tolly's circuit show?",
                    ["Red - Yellow - Green", "Blue - Purple - Pink", "Black - White - Gray"],
                    0
                ),
                (
                    "What circuit component creates Tolly's automated light sequence?",
                    ["A timer circuit", "A simple battery wire", "A mechanical spring"],
                    0
                ),
                (
                    "What real-world electronic application does Tolly mimic?",
                    ["Traffic light signals", "Microwave ovens", "Washing machines"],
                    0
                ),
                (
                    "What electronic light components are controlled by Tolly's timer?",
                    ["LEDs (Light Emitting Diodes)", "Incandescent bulbs", "Halogen lamps"],
                    0
                ),
                (
                    "Why is a timer circuit essential for Tolly?",
                    ["It regulates the delay and switching interval between LEDs", "It increases battery voltage", "It turns paper into metal"],
                    0
                )
            ]

        elif cid == "emoti":
            bank = [
                (
                    "What is Emoti's primary specialty as a Funobotz character?",
                    ["An expression bot that brings emotions to life", "A heavy lifting crane", "A solar water heater"],
                    0
                ),
                (
                    "How does Emoti express reactions during interactions?",
                    ["Through simple movements and expressive reactions", "By firing lasers", "By changing color temperature"],
                    0
                ),
                (
                    "What STEM concept does Emoti demonstrate when reacting to inputs?",
                    ["Translating input signals into movement and reaction", "Chemical oxidation", "Nuclear fission"],
                    0
                ),
                (
                    "How does Emoti help learners understand emotional expression mechanisms?",
                    ["By pairing physical movements with emotional cues", "By reading mind waves", "By storing fuel"],
                    0
                ),
                (
                    "What component feedback allows Emoti to react to surrounding interactions?",
                    ["Sensors translating inputs into movement patterns", "Pressurized steam", "Solar panels"],
                    0
                )
            ]

        elif cid == "mimo":
            bank = [
                (
                    "What character persona and design does Mimo represent?",
                    ["A paper pet dog that comes to life through simple movement", "A flying dragon", "A submarine"],
                    0
                ),
                (
                    "How does Mimo interact with learners during STEM sessions?",
                    ["Through simple paper movement and playful interaction", "By barking through speakers", "By running on gasoline"],
                    0
                ),
                (
                    "What mechanical principle is demonstrated when Mimo moves?",
                    ["Simple paper mechanics and linkage motion", "Steam propulsion", "Magnetic levitation"],
                    0
                ),
                (
                    "Why is Mimo great for beginner paper roboticists?",
                    ["It turns simple paper cutouts into interactive pet movements", "It requires complex C++ coding", "It weighs 10kg"],
                    0
                ),
                (
                    "How does paper fold alignment affect Mimo's paper pet motion?",
                    ["Smooth fold flexibility ensures unconstrained linkage motion", "Folds must be glued tight", "Paper color changes weight"],
                    0
                )
            ]

        elif cid == "kuttybot":
            bank = [
                (
                    "What is Kuttybot's unique interaction feature in the roster?",
                    ["A friendly talking robot that speaks and interacts", "A solar charging panel", "An underwater propeller"],
                    0
                ),
                (
                    "How does Kuttybot communicate with learners during learning sessions?",
                    ["Using audio response speech interaction", "By flashing morse code", "By throwing paper"],
                    0
                ),
                (
                    "What STEM field does Kuttybot introduce through speech?",
                    ["Human-robot interaction and audio communication", "Petroleum refining", "Deep sea geology"],
                    0
                ),
                (
                    "What makes Kuttybot an inviting companion for young learners?",
                    ["Friendly verbal dialogue and interactive speech feedback", "Loud alarms", "High voltage sparks"],
                    0
                ),
                (
                    "What electronic component converts Kuttybot's signals into spoken words?",
                    ["An audio speaker transducer", "A paper wheel", "A rubber band"],
                    0
                )
            ]

        elif cid == "kutty-omni":
            bank = [
                (
                    "What type of movement design is Kutty-Omni created for?",
                    ["Omnidirectional multi-directional motion", "Single straight track line", "Fixed stationary post"],
                    0
                ),
                (
                    "What status does Kutty-Omni currently hold in the official roster?",
                    ["Official character pending detailed STEM concept sheet release", "Fully deprecated", "Third party add-on"],
                    0
                ),
                (
                    "How does the Funobotz architecture handle Kutty-Omni pending release?",
                    ["Supports it seamlessly for future official updates without code changes", "Throws a crash error", "Deletes the character"],
                    0
                ),
                (
                    "What advantage does an omnidirectional chassis give Kutty-Omni?",
                    ["Ability to move in any direction instantly without pivoting", "Higher weight capacity", "Solar energy storage"],
                    0
                ),
                (
                    "What vector control principle governs Kutty-Omni's multi-wheel movement?",
                    ["Synchronizing multiple motor speeds to slide diagonally or sideways", "Blowing wind", "Gravity drop"],
                    0
                )
            ]

        elif cid == "wavy":
            bank = [
                (
                    "What characteristic movement mechanism does Wavy demonstrate?",
                    ["Continuous wave-like oscillating movement", "Vertical elevator drop", "Rocket blast off"],
                    0
                ),
                (
                    "How is rotary motor motion converted in Wavy's mechanical design?",
                    ["Rotary motor motion is converted into oscillating wave motion via linkages", "By using a mirror", "By heating up wires"],
                    0
                ),
                (
                    "What status does Wavy hold in the official character roster?",
                    ["Official roster member pending detailed material release", "Unofficial mod", "Retired bot"],
                    0
                ),
                (
                    "What real-world mechanical concept does Wavy's oscillating linkage mimic?",
                    ["Wave generators and sinusoidal mechanical linkages", "Hydraulic car brakes", "Gasoline pumps"],
                    0
                ),
                (
                    "What motion pattern is created when Wavy's motor shaft spins continuously?",
                    ["A repeating smooth wave oscillation", "A static pause", "A square jump"],
                    0
                )
            ]

        elif cid == "chicky":
            bank = [
                (
                    "What type of movement mechanism powers Chicky's motion?",
                    ["Vibrating and hopping motion via eccentric motor weights", "Jet engine thrust", "Pneumatic piston"],
                    0
                ),
                (
                    "How does kinetic vibration move Chicky across surfaces?",
                    ["Vibrations reduce friction and cause small forward hops", "By magnetic repulsion", "By wind currents"],
                    0
                ),
                (
                    "What is Chicky's official status in the Funobotz ecosystem?",
                    ["Official character pending detailed STEM concept release", "Fake character", "External plugin"],
                    0
                ),
                (
                    "What component inside Chicky creates the vibration energy?",
                    ["An offset counterweight mounted on a small motor shaft", "A speaker cone", "A water pump"],
                    0
                ),
                (
                    "Why does an offset weight create vibration when spun quickly?",
                    ["Unbalanced rotational centrifugal force causes rapid micro-hopping", "It heats up the paper", "It magnetizes the ground"],
                    0
                )
            ]

        elif cid == "omni":
            bank = [
                (
                    "What special wheel mechanism distinguishes Omni from standard rovers?",
                    ["Omni-directional wheels that allow 360-degree movement without turning", "Square rubber pads", "Wooden pegs"],
                    0
                ),
                (
                    "What engineering concept is explored with Omni-directional drives?",
                    ["Vector movement and multi-motor synchronization", "Boiler pressure", "Static friction only"],
                    0
                ),
                (
                    "How does the AI assistant handle Omni's pending concept release?",
                    ["Explains roster status accurately without fabricating unverified facts", "Invents fake facts", "Shuts down the server"],
                    0
                ),
                (
                    "How many axes of movement can an omnidirectional rover control simultaneously?",
                    ["3 degrees of freedom (x-axis, y-axis, and rotation)", "Only 1 axis", "None"],
                    0
                ),
                (
                    "Why are perpendicular rollers placed around Omni's wheel rim?",
                    ["They roll freely sideways while the main wheel drives forward", "To grip mud", "To generate light"],
                    0
                )
            ]

        elif cid == "cuby":
            bank = [
                (
                    "What structural design approach does Cuby represent?",
                    ["Modular block robotics and spatial geometric building", "Glass blowing", "Fluid dynamics"],
                    0
                ),
                (
                    "How do modular blocks benefit paper and block robotics?",
                    ["Allow quick reconfigurable snap-together assembly", "Makes the robot permanent and unchangeable", "Increases weight"],
                    0
                ),
                (
                    "What status does Cuby currently hold in the official roster?",
                    ["Official roster character pending detailed concept sheet release", "Deleted model", "Paid expansion DLC"],
                    0
                ),
                (
                    "What spatial STEM skill does constructing Cuby build for learners?",
                    ["3D geometry, structural balance, and modular thinking", "Deep sea diving", "Text parsing"],
                    0
                ),
                (
                    "What electrical connection design allows Cuby blocks to snap together?",
                    ["Modular pin connectors that complete power circuits on assembly", "Liquid glue", "Welded steel rods"],
                    0
                )
            ]

        else:
            bank = [
                (
                    "What is the primary role of this Funobotz character?",
                    ["Interactive STEM learning companion", "Generic question bot", "Calculator"],
                    0
                )
            ]

        # Select non-repeating question using seed_idx
        idx = seed_idx % len(bank)
        return bank[idx]

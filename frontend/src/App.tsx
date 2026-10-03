import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { CustomerAccessCheck } from './components/CustomerAccessCheck';
import { ProfileSetup } from './components/ProfileSetup';
import { CharacterTopicRouter } from './components/CharacterTopicRouter';
import { ChatInterface } from './components/ChatInterface';
import { MiniChallenge } from './components/MiniChallenge';
import { DemoPanel } from './components/DemoPanel';
import { WidgetView } from './components/WidgetView';
import { LearnerProfile, CustomerInfo, Character, ChatMessage } from './types';
import {
  createSession,
  fetchCustomerInfo,
  fetchCharacters,
  sendChatMessage,
  updateLearnerProfile
} from './services/apiService';

export const App: React.FC = () => {
  const [sessionId, setSessionId] = useState<string>('');
  const [profile, setProfile] = useState<LearnerProfile>({
    learner_id: 'L-01',
    name: 'Spark Learner',
    age: 8,
    interest: 'motors',
    starting_knowledge: 'Beginner',
    current_level: 0,
    current_topic: 'motors',
    active_character: 'quacky',
    customer_id: 'FZ-HACK-001'
  });

  const [customerInfo, setCustomerInfo] = useState<CustomerInfo | null>(null);
  const [characters, setCharacters] = useState<Character[]>([]);
  const [activeChar, setActiveChar] = useState<Character | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [demoMode, setDemoMode] = useState<boolean>(true);
  const [showWidgetView, setShowWidgetView] = useState<boolean>(false);
  const [score, setScore] = useState<number>(0);

  const [latestCheck, setLatestCheck] = useState<{
    question: string;
    options: string[];
    correctOption: number;
  }>({
    question: "How does Quacky's BO motor create movement?",
    options: ["By transforming electrical energy into mechanical movement", "By freezing water", "By shining a laser"],
    correctOption: 0
  });

  // Initialize Session & Load Initial Data
  useEffect(() => {
    async function init() {
      try {
        const sess = await createSession(profile);
        setSessionId(sess.session_id);

        const chars = await fetchCharacters();
        setCharacters(chars);

        const active = chars.find(c => c.id === profile.active_character) || chars[0];
        setActiveChar(active || null);

        const cInfo = await fetchCustomerInfo(profile.customer_id);
        setCustomerInfo(cInfo);

        // Initial welcome message
        setMessages([
          {
            id: 'init-1',
            sender: 'bot',
            text: `Hello! I'm ${active?.name || 'Quacky'}, your Funobotz STEM learning companion!\nI can help you explore ${profile.current_topic} tailored to your age and starting knowledge.`,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            concept: profile.current_topic,
            difficulty: profile.starting_knowledge
          }
        ]);
      } catch (e) {
        console.error("Initialization error:", e);
      }
    }
    init();
  }, []);

  // Sync Customer Info on Customer ID change
  const handleSelectCustomer = async (cid: string) => {
    const updatedProfile = { ...profile, customer_id: cid };
    setProfile(updatedProfile);
    try {
      const info = await fetchCustomerInfo(cid);
      setCustomerInfo(info);
      if (sessionId) {
        await updateLearnerProfile(sessionId, updatedProfile);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Sync Profile Changes
  const handleUpdateProfile = async (updated: LearnerProfile) => {
    setProfile(updated);
    const active = characters.find(c => c.id === updated.active_character) || activeChar;
    setActiveChar(active || null);
    try {
      if (sessionId) {
        await updateLearnerProfile(sessionId, updated);
      }
    } catch (e) {
      console.error(e);
    }
  };

  // Select Character Companion
  const handleSelectCharacter = async (charId: string) => {
    const active = characters.find(c => c.id === charId) || null;
    setActiveChar(active);
    const updated = { ...profile, active_character: charId };
    setProfile(updated);
    if (sessionId) {
      await updateLearnerProfile(sessionId, updated);
    }
  };

  // Handle User Message Sending
  const handleSendMessage = async (msgText: string, requestedChar?: string) => {
    const userMsg: ChatMessage = {
      id: `usr_${Date.now()}`,
      sender: 'user',
      text: msgText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await sendChatMessage({
        session_id: sessionId,
        message: msgText,
        customer_id: profile.customer_id,
        learner_profile: profile,
        requested_character: requestedChar || profile.active_character
      });

      const botMsg: ChatMessage = {
        id: `bot_${Date.now()}`,
        sender: 'bot',
        text: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        concept: res.concept,
        difficulty: res.difficulty,
        options: res.options,
        correctOption: res.correct_option,
        nextStep: res.next_step,
        accessGranted: res.access_granted,
        accessNotice: res.access_notice,
        unsupportedNotice: res.unsupported_fact_notice,
        escalationTriggered: res.escalation_triggered,
        clarificationNeeded: res.clarification_needed,
        clarificationOptions: res.clarification_options
      };

      setMessages(prev => [...prev, botMsg]);

      // Update Profile Level / Topic if changed by backend
      setProfile(prev => ({
        ...prev,
        starting_knowledge: res.difficulty as any,
        current_topic: res.active_topic,
        active_character: res.active_character,
        current_level: res.difficulty === 'Beginner' ? 0 : res.difficulty === 'Intermediate' ? 1 : 2
      }));

      const newActive = characters.find(c => c.id === res.active_character);
      if (newActive) setActiveChar(newActive);

      if (res.check_question && res.options) {
        setLatestCheck({
          question: res.check_question,
          options: res.options,
          correctOption: res.correct_option !== undefined ? res.correct_option : 0
        });
      }
    } catch (e) {
      console.error(e);
      setMessages(prev => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: 'bot',
          text: 'Connection notice: Could not reach backend server. Ensure FastAPI server is running at http://127.0.0.1:8000',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Handle Judge Demo Scenario execution
  const handleScenarioExecuted = (scenarioData: any) => {
    const res = scenarioData.response;
    const prof = scenarioData.profile;

    setProfile(prof);
    setSessionId(scenarioData.session_id);

    const active = characters.find(c => c.id === res.active_character) || activeChar;
    setActiveChar(active || null);

    setMessages([
      {
        id: `scen_req_${Date.now()}`,
        sender: 'user',
        text: scenarioData.request_message,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      },
      {
        id: `scen_res_${Date.now()}`,
        sender: 'bot',
        text: res.answer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        concept: res.concept,
        difficulty: res.difficulty,
        options: res.options,
        correctOption: res.correct_option,
        nextStep: res.next_step,
        accessGranted: res.access_granted,
        accessNotice: res.access_notice,
        unsupportedNotice: res.unsupported_fact_notice,
        escalationTriggered: res.escalation_triggered,
        clarificationNeeded: res.clarification_needed,
        clarificationOptions: res.clarification_options
      }
    ]);

    if (res.check_question && res.options) {
      setLatestCheck({
        question: res.check_question,
        options: res.options,
        correctOption: res.correct_option !== undefined ? res.correct_option : 0
      });
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar
        profile={profile}
        customerInfo={customerInfo}
        demoMode={demoMode}
        setDemoMode={setDemoMode}
        showWidget={showWidgetView}
        setShowWidget={setShowWidgetView}
      />

      <div className="app-container">
        {demoMode && <DemoPanel onScenarioExecuted={handleScenarioExecuted} />}

        {showWidgetView ? (
          <WidgetView />
        ) : (
          <>
            <div className="main-grid">
              {/* Left Column: Access & Profile Setup */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <CustomerAccessCheck
                  profile={profile}
                  customerInfo={customerInfo}
                  onSelectCustomer={handleSelectCustomer}
                />

                <ProfileSetup
                  profile={profile}
                  onUpdateProfile={handleUpdateProfile}
                />

                <CharacterTopicRouter
                  characters={characters}
                  profile={profile}
                  accessibleCharacters={customerInfo?.accessible_characters || []}
                  onSelectCharacter={handleSelectCharacter}
                />
              </div>

              {/* Right Column: Chat & Mini Challenge */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                <ChatInterface
                  messages={messages}
                  activeCharacter={activeChar}
                  profile={profile}
                  onSendMessage={handleSendMessage}
                  onOptionSelect={(opt) => handleSendMessage(opt)}
                  loading={loading}
                />

                <MiniChallenge
                  sessionId={sessionId}
                  question={latestCheck.question}
                  options={latestCheck.options}
                  correctOption={latestCheck.correctOption}
                  score={score}
                  onScoreUpdate={(s) => setScore(s)}
                />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default App;

import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage, Character, LearnerProfile } from '../types';
import { Send, Sparkles, HelpCircle, ShieldAlert, ArrowUpRight, Zap, RefreshCw } from 'lucide-react';

interface Props {
  messages: ChatMessage[];
  activeCharacter: Character | null;
  profile: LearnerProfile;
  onSendMessage: (msg: string, requestedChar?: string) => void;
  onOptionSelect: (optionText: string) => void;
  loading: boolean;
}

export const ChatInterface: React.FC<Props> = ({
  messages,
  activeCharacter,
  profile,
  onSendMessage,
  onOptionSelect,
  loading
}) => {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || loading) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  return (
    <div className="glass-panel chat-container">
      {/* Companion Header */}
      <div className="chat-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <span style={{ fontSize: '2.2rem' }}>{activeCharacter?.avatar || '🤖'}</span>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <h3 style={{ fontSize: '1.2rem', margin: 0 }}>{activeCharacter?.name || 'Funobotz Companion'}</h3>
              <span className="badge badge-purple" style={{ fontSize: '0.65rem' }}>
                Topic: {profile.current_topic}
              </span>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#94a3b8', margin: 0 }}>
              {activeCharacter?.official_context || 'Personalized STEM Learning Buddy'}
            </p>
          </div>
        </div>

        <div style={{ textAlign: 'right' }}>
          <span className="badge badge-amber" style={{ fontSize: '0.75rem' }}>
            Level: {profile.starting_knowledge} ({profile.current_level})
          </span>
        </div>
      </div>

      {/* Messages Feed */}
      <div className="chat-messages">
        {messages.map(msg => {
          const isUser = msg.sender === 'user';

          return (
            <div key={msg.id} className={`chat-bubble ${isUser ? 'user' : 'bot'}`}>
              {!isUser && msg.escalationTriggered && (
                <div style={{ marginBottom: '0.5rem' }}>
                  <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>
                    <Zap size={12} /> Complexity Escalated
                  </span>
                </div>
              )}

              {!isUser && msg.accessNotice && (
                <div style={{ marginBottom: '0.5rem', background: 'rgba(244,63,94,0.15)', border: '1px solid rgba(244,63,94,0.3)', padding: '0.5rem', borderRadius: '8px', fontSize: '0.8rem', color: '#fda4af' }}>
                  <ShieldAlert size={14} style={{ inlineSize: '14px', marginRight: '0.3rem' }} />
                  {msg.accessNotice}
                </div>
              )}

              {!isUser && msg.unsupportedNotice && (
                <div style={{ marginBottom: '0.5rem', background: 'rgba(245,158,11,0.15)', border: '1px solid rgba(245,158,11,0.3)', padding: '0.5rem', borderRadius: '8px', fontSize: '0.8rem', color: '#fcd34d' }}>
                  <HelpCircle size={14} style={{ inlineSize: '14px', marginRight: '0.3rem' }} />
                  {msg.unsupportedNotice}
                </div>
              )}

              <div style={{ whiteSpace: 'pre-line' }}>{msg.text}</div>

              {/* Interactive Options / Clarification Pills */}
              {msg.options && msg.options.length > 0 && (
                <div style={{ marginTop: '0.85rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {msg.options.map((opt, idx) => (
                    <button
                      key={idx}
                      className="btn btn-secondary btn-pill"
                      style={{ textTransform: 'none', justifyContent: 'flex-start', fontSize: '0.82rem', padding: '0.4rem 0.85rem' }}
                      onClick={() => onOptionSelect(opt)}
                    >
                      <ArrowUpRight size={14} color="#a855f7" />
                      {opt}
                    </button>
                  ))}
                </div>
              )}

              <div style={{ fontSize: '0.65rem', color: isUser ? 'rgba(255,255,255,0.7)' : '#64748b', marginTop: '0.4rem', textAlign: 'right' }}>
                {msg.timestamp}
              </div>
            </div>
          );
        })}

        {loading && (
          <div className="chat-bubble bot" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <RefreshCw className="spin" size={16} color="#a855f7" />
            <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Thinking & adapting response...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Action Suggestion Bar */}
      <div style={{ padding: '0.5rem 1.5rem', background: 'rgba(15,23,42,0.6)', borderTop: '1px solid var(--border-glass)', display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.75rem', color: '#94a3b8', alignSelf: 'center' }}>Test Scenarios:</span>
        <button 
          className="btn btn-secondary btn-pill" 
          style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
          onClick={() => onSendMessage("I already know this.")}
        >
          ⚡ "I already know this" (Escalate)
        </button>

        <button 
          className="btn btn-secondary btn-pill" 
          style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
          onClick={() => onSendMessage("Actually I want to learn about light with Petalo!")}
        >
          💡 "Switch to Light (Petalo)"
        </button>

        <button 
          className="btn btn-secondary btn-pill" 
          style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
          onClick={() => onSendMessage("Why does it move?")}
        >
          ❓ "Why does it move?" (Clarification)
        </button>

        <button 
          className="btn btn-secondary btn-pill" 
          style={{ fontSize: '0.72rem', padding: '0.2rem 0.6rem' }}
          onClick={() => onSendMessage("What is Tiko's favorite food?")}
        >
          🚫 "What is favorite food?" (Strict Grounding)
        </button>
      </div>

      {/* Input Bar */}
      <form onSubmit={handleSubmit} className="chat-input-area">
        <input
          type="text"
          className="chat-input"
          placeholder={`Ask ${activeCharacter?.name || 'companion'} a STEM question...`}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button type="submit" className="btn btn-primary" disabled={loading || !inputText.trim()}>
          <Send size={16} />
          Send
        </button>
      </form>
    </div>
  );
};

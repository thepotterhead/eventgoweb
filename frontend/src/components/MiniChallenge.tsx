import React, { useState } from 'react';
import { Award, CheckCircle2, XCircle, HelpCircle, Trophy } from 'lucide-react';
import { submitLearningCheck } from '../services/apiService';

interface Props {
  sessionId: string;
  question: string;
  options: string[];
  correctOption: number;
  score: number;
  onScoreUpdate: (newScore: number) => void;
}

export const MiniChallenge: React.FC<Props> = ({
  sessionId,
  question,
  options,
  correctOption,
  score,
  onScoreUpdate
}) => {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  const handleSelect = async (idx: number) => {
    if (submitted) return;
    setSelectedIdx(idx);
    try {
      const res = await submitLearningCheck({
        session_id: sessionId,
        question: question,
        selected_option: idx,
        correct_option: correctOption
      });
      setSubmitted(true);
      setFeedback(res.feedback);
      setIsCorrect(res.is_correct);
      if (res.is_correct) {
        onScoreUpdate(score + res.score_delta);
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
        <h3 style={{ fontSize: '1.05rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Trophy size={18} color="#f59e0b" />
          Mini Challenge / Understanding Check
        </h3>
        <span className="badge badge-amber" style={{ fontSize: '0.75rem' }}>
          Score: {score} XP
        </span>
      </div>

      <div style={{ background: 'rgba(30, 41, 59, 0.6)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--border-glass)' }}>
        <p style={{ fontSize: '0.9rem', fontWeight: 600, color: '#f8fafc', marginBottom: '0.75rem' }}>
          ❓ {question}
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {options.map((opt, idx) => {
            let bg = 'rgba(51, 65, 85, 0.4)';
            let borderColor = 'var(--border-glass)';

            if (submitted) {
              if (idx === correctOption) {
                bg = 'rgba(16, 185, 129, 0.25)';
                borderColor = '#10b981';
              } else if (idx === selectedIdx) {
                bg = 'rgba(244, 63, 94, 0.25)';
                borderColor = '#f43f5e';
              }
            }

            return (
              <button
                key={idx}
                disabled={submitted}
                onClick={() => handleSelect(idx)}
                style={{
                  textAlign: 'left',
                  padding: '0.6rem 0.85rem',
                  borderRadius: '8px',
                  background: bg,
                  border: `1px solid ${borderColor}`,
                  color: '#fff',
                  cursor: submitted ? 'default' : 'pointer',
                  fontSize: '0.85rem',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  justify: 'space-between',
                  alignItems: 'center'
                }}
              >
                <span>{opt}</span>
                {submitted && idx === correctOption && <CheckCircle2 size={16} color="#10b981" />}
                {submitted && idx === selectedIdx && idx !== correctOption && <XCircle size={16} color="#f43f5e" />}
              </button>
            );
          })}
        </div>

        {submitted && feedback && (
          <div style={{ marginTop: '0.85rem', padding: '0.6rem 0.85rem', borderRadius: '8px', background: isCorrect ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)', border: `1px solid ${isCorrect ? '#10b981' : '#f43f5e'}`, fontSize: '0.82rem', color: isCorrect ? '#34d399' : '#fda4af' }}>
            {feedback}
          </div>
        )}
      </div>
    </div>
  );
};

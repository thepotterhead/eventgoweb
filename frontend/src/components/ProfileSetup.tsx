import React from 'react';
import { LearnerProfile } from '../types';
import { User, Sparkles, BookOpen, Compass } from 'lucide-react';

interface Props {
  profile: LearnerProfile;
  onUpdateProfile: (updated: LearnerProfile) => void;
}

const SYNTHETIC_PROFILES: Record<string, Partial<LearnerProfile> & { desc: string }> = {
  'L-01': {
    name: 'Spark Learner',
    age: 8,
    interest: 'light',
    starting_knowledge: 'Beginner',
    current_level: 0,
    active_character: 'petalo',
    desc: 'Age 8, light & colourful builds, first-time STEM learner.'
  },
  'L-02': {
    name: 'Motion Explorer',
    age: 11,
    interest: 'motors',
    starting_knowledge: 'Intermediate',
    current_level: 1,
    active_character: 'tiko',
    desc: 'Age 11, movement & machines, understands basic battery connections.'
  },
  'L-03': {
    name: 'Story Discoverer',
    age: 9,
    interest: 'stories',
    starting_knowledge: 'Beginner',
    current_level: 0,
    active_character: 'quacky',
    desc: 'Age 9, stories & characters, needs short simple explanations.'
  },
  'L-04': {
    name: 'Circuit Master',
    age: 12,
    interest: 'electronics',
    starting_knowledge: 'Advanced',
    current_level: 2,
    active_character: 'tolly',
    desc: 'Age 12, electronics & circuits, wants deeper technical reasoning.'
  },
  'L-05': {
    name: 'Open Inquirer',
    age: 10,
    interest: 'open-ended',
    starting_knowledge: 'Beginner',
    current_level: 0,
    active_character: 'quacky',
    desc: 'Age 10, no stated STEM preference, explores via open questions.'
  }
};

export const ProfileSetup: React.FC<Props> = ({ profile, onUpdateProfile }) => {
  const handleSelectPreset = (pid: string) => {
    const p = SYNTHETIC_PROFILES[pid];
    if (!p) return;
    onUpdateProfile({
      ...profile,
      learner_id: pid,
      name: p.name || profile.name,
      age: p.age || profile.age,
      interest: p.interest || profile.interest,
      starting_knowledge: p.starting_knowledge || profile.starting_knowledge,
      current_level: p.current_level !== undefined ? p.current_level : profile.current_level,
      active_character: p.active_character || profile.active_character,
      current_topic: p.interest || profile.current_topic
    });
  };

  return (
    <div className="glass-panel" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <User size={18} color="#a855f7" />
          Learner Profile & Adaptation Setup
        </h3>
        <span className="badge badge-purple">Active Profile: {profile.learner_id}</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))', gap: '0.75rem', marginBottom: '1rem' }}>
        {Object.entries(SYNTHETIC_PROFILES).map(([pid, p]) => {
          const isSelected = profile.learner_id === pid;
          return (
            <div
              key={pid}
              onClick={() => handleSelectPreset(pid)}
              style={{
                padding: '0.75rem',
                borderRadius: '10px',
                background: isSelected ? 'rgba(168, 85, 247, 0.2)' : 'rgba(30, 41, 59, 0.4)',
                border: isSelected ? '1px solid #a855f7' : '1px solid var(--border-glass)',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ fontSize: '0.85rem' }}>{pid}: {p.name}</strong>
                <span style={{ fontSize: '0.75rem', color: '#cbd5e1' }}>Age {p.age}</span>
              </div>
              <p style={{ fontSize: '0.72rem', color: '#94a3b8', marginTop: '0.35rem' }}>
                {p.desc}
              </p>
            </div>
          );
        })}
      </div>

      {/* Manual Fine-Tuning Controls */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '0.75rem', paddingTop: '0.75rem', borderTop: '1px solid var(--border-glass)' }}>
        <div>
          <label style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'block', marginBottom: '0.25rem' }}>Learner Age</label>
          <select
            value={profile.age}
            onChange={(e) => onUpdateProfile({ ...profile, age: parseInt(e.target.value) })}
            style={{ width: '100%', padding: '0.4rem', borderRadius: '8px', background: '#1e293b', color: '#fff', border: '1px solid var(--border-glass)' }}
          >
            {[7, 8, 9, 10, 11, 12, 13, 14].map(a => (
              <option key={a} value={a}>Age {a}</option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'block', marginBottom: '0.25rem' }}>Starting Knowledge</label>
          <select
            value={profile.starting_knowledge}
            onChange={(e) => {
              const val = e.target.value as 'Beginner' | 'Intermediate' | 'Advanced';
              const lvl = val === 'Beginner' ? 0 : val === 'Intermediate' ? 1 : 2;
              onUpdateProfile({ ...profile, starting_knowledge: val, current_level: lvl });
            }}
            style={{ width: '100%', padding: '0.4rem', borderRadius: '8px', background: '#1e293b', color: '#fff', border: '1px solid var(--border-glass)' }}
          >
            <option value="Beginner">Beginner (Level 0)</option>
            <option value="Intermediate">Intermediate (Level 1)</option>
            <option value="Advanced">Advanced (Level 2)</option>
          </select>
        </div>

        <div>
          <label style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'block', marginBottom: '0.25rem' }}>Current Interest</label>
          <select
            value={profile.interest}
            onChange={(e) => onUpdateProfile({ ...profile, interest: e.target.value, current_topic: e.target.value })}
            style={{ width: '100%', padding: '0.4rem', borderRadius: '8px', background: '#1e293b', color: '#fff', border: '1px solid var(--border-glass)' }}
          >
            <option value="motors">Motors & Motion</option>
            <option value="light">Light & Discovery</option>
            <option value="circuits">Circuits & Timing</option>
            <option value="stories">Story & Reactions</option>
          </select>
        </div>
      </div>
    </div>
  );
};

import React from 'react';
import { Character, LearnerProfile } from '../types';
import { Bot, CheckCircle, Info, Lock } from 'lucide-react';

interface Props {
  characters: Character[];
  profile: LearnerProfile;
  accessibleCharacters: string[];
  onSelectCharacter: (charId: string) => void;
}

export const CharacterTopicRouter: React.FC<Props> = ({
  characters,
  profile,
  accessibleCharacters,
  onSelectCharacter
}) => {
  return (
    <div className="glass-panel" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Bot size={18} color="#06b6d4" />
          Official Funobotz Character Roster (12 Companions)
        </h3>
        <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Select Companion</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '0.75rem', maxHeight: '420px', overflowY: 'auto', paddingRight: '0.25rem' }}>
        {characters.map(char => {
          const isActive = profile.active_character === char.id;
          const isAccessible = accessibleCharacters.length === 0 || accessibleCharacters.includes(char.id) || char.status !== 'mapped';

          return (
            <div
              key={char.id}
              className={`character-card ${isActive ? 'active' : ''}`}
              onClick={() => onSelectCharacter(char.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '1.8rem' }}>{char.avatar}</span>
                {char.status === 'mapped' ? (
                  <span className="badge badge-emerald" style={{ fontSize: '0.6rem', padding: '0.1rem 0.35rem' }}>
                    Mapped
                  </span>
                ) : char.status === 'behaviour_only' ? (
                  <span className="badge badge-purple" style={{ fontSize: '0.6rem', padding: '0.1rem 0.35rem' }}>
                    Behaviour
                  </span>
                ) : (
                  <span className="badge badge-amber" style={{ fontSize: '0.6rem', padding: '0.1rem 0.35rem' }}>
                    Pending
                  </span>
                )}
              </div>

              <strong style={{ fontSize: '0.9rem', display: 'block', marginBottom: '0.2rem' }}>
                {char.name}
              </strong>
              <div style={{ fontSize: '0.72rem', color: '#94a3b8', lineHeight: 1.2 }}>
                {char.tagline}
              </div>

              {!isAccessible && (
                <div style={{ marginTop: '0.4rem', fontSize: '0.65rem', color: '#f43f5e', display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                  <Lock size={10} /> Kit Not Purchased
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

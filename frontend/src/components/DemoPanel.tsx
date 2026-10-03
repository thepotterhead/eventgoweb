import React from 'react';
import { Play, Sparkles, CheckCircle, ShieldAlert, Cpu } from 'lucide-react';
import { triggerDemoScenario } from '../services/apiService';

interface Props {
  onScenarioExecuted: (scenarioData: any) => void;
}

const HACKATHON_SCENARIOS = [
  {
    id: 1,
    title: '1. Mechanical Motion & Motors',
    desc: 'Tiko tail thread movement & motor circuit.',
    tag: 'Grounded Concept'
  },
  {
    id: 2,
    title: '2. Light & Discovery Shifting',
    desc: 'Topic shift from motors to Petalo light.',
    tag: 'Interest Shifting'
  },
  {
    id: 3,
    title: '3. Product Access & Safety',
    desc: 'Managing product permissions safely.',
    tag: 'Access Control'
  },
  {
    id: 4,
    title: '4. Ambiguity & Clarification',
    desc: 'Resolving "Why does it move?" questions.',
    tag: 'Ambiguity Router'
  },
  {
    id: 5,
    title: '5. Grounding & Fact Refusal',
    desc: 'Refusing to invent unapproved facts.',
    tag: 'Strict Grounding'
  },
  {
    id: 6,
    title: '6. Advanced Concept Escalation',
    desc: 'Deepening depth when learner knows basics.',
    tag: 'Dynamic Depth'
  },
  {
    id: 7,
    title: '7. Roster Character Expansion',
    desc: 'Routing unreleased characters (Cuby).',
    tag: '12-Character Roster'
  },
  {
    id: 8,
    title: '8. Multi-Product Circuits',
    desc: 'Quacky, Tiko & Tolly circuit integration.',
    tag: 'Multi-Product'
  }
];

export const DemoPanel: React.FC<Props> = ({ onScenarioExecuted }) => {
  const handleRunScenario = async (id: number) => {
    try {
      const data = await triggerDemoScenario(id);
      onScenarioExecuted(data);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="demo-banner">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#c084fc' }}>
            <Cpu size={20} />
            INTERACTIVE LEARNING SCENARIO PRESETS
          </h3>
          <p style={{ fontSize: '0.8rem', color: '#cbd5e1' }}>
            Click any scenario button below to instantly execute and verify interactive STEM learning scenarios.
          </p>
        </div>
        <span className="badge badge-purple">8 Presets Ready</span>
      </div>

      <div className="scenario-btn-grid">
        {HACKATHON_SCENARIOS.map(s => (
          <button
            key={s.id}
            className="scenario-btn"
            onClick={() => handleRunScenario(s.id)}
          >
            <div style={{ fontWeight: 700, fontSize: '0.82rem', marginBottom: '0.2rem', color: '#fff', display: 'flex', justifyContent: 'space-between' }}>
              <span>{s.title}</span>
              <Play size={12} color="#a855f7" />
            </div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8', lineHeight: 1.2 }}>
              {s.desc}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

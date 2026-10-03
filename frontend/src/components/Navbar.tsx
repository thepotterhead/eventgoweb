import React from 'react';
import { LearnerProfile, CustomerInfo } from '../types';
import { Sparkles, ShieldCheck, UserCheck, Bot, LayoutDashboard, Code } from 'lucide-react';

interface NavbarProps {
  profile: LearnerProfile;
  customerInfo: CustomerInfo | null;
  demoMode: boolean;
  setDemoMode: (val: boolean) => void;
  showWidget: boolean;
  setShowWidget: (val: boolean) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  profile,
  customerInfo,
  demoMode,
  setDemoMode,
  showWidget,
  setShowWidget
}) => {
  return (
    <header className="navbar">
      <div className="nav-brand">
        <span style={{ fontSize: '1.8rem' }}>🤖</span>
        <span className="gradient-text">FUNOBOTZ</span>
        <span style={{ fontSize: '0.9rem', color: '#94a3b8', fontWeight: 500 }}>STEM Companion</span>
      </div>

      <div className="nav-controls">
        <div className="badge badge-purple">
          <UserCheck size={14} />
          {profile.name} (Age {profile.age})
        </div>

        <div className="badge badge-emerald">
          <ShieldCheck size={14} />
          Account: {profile.customer_id}
        </div>

        <div className="badge badge-amber">
          <Sparkles size={14} />
          Level {profile.current_level} ({profile.starting_knowledge})
        </div>

        <button 
          className={`btn ${showWidget ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setShowWidget(!showWidget)}
          title="Toggle Embeddable Widget View"
        >
          <Code size={16} />
          {showWidget ? 'Full App View' : 'Embed Widget Demo'}
        </button>

        <button 
          className={`btn ${demoMode ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setDemoMode(!demoMode)}
        >
          <LayoutDashboard size={16} />
          {demoMode ? 'Hide Demo Scenarios' : 'Interactive Scenarios'}
        </button>
      </div>
    </header>
  );
};

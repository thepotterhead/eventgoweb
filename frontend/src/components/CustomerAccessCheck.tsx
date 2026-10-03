import React from 'react';
import { CustomerInfo, LearnerProfile } from '../types';
import { ShieldAlert, ShieldCheck, ShoppingBag, Lock } from 'lucide-react';

interface Props {
  profile: LearnerProfile;
  customerInfo: CustomerInfo | null;
  onSelectCustomer: (customerId: string) => void;
}

const CUSTOMER_DATASETS: Record<string, { name: string; products: string[] }> = {
  'FZ-HACK-001': { name: 'Single/Dual Product Account', products: ['petalo', 'quacky'] },
  'FZ-HACK-002': { name: 'Mechanic Explorer', products: ['tiko'] },
  'FZ-HACK-003': { name: 'Circuits & Light Enthusiast', products: ['tolly', 'petalo'] },
  'FZ-HACK-004': { name: 'Full STEM Robotics Bundle', products: ['quacky', 'tiko', 'tolly'] },
  'FZ-HACK-005': { name: 'No Valid Purchased Product Account', products: [] },
};

export const CustomerAccessCheck: React.FC<Props> = ({
  profile,
  customerInfo,
  onSelectCustomer
}) => {
  return (
    <div className="glass-panel" style={{ padding: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck size={18} color="#10b981" />
          Customer Access Control Layer
        </h3>
        <span style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Synthetic Hackathon Dataset</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem' }}>
        {Object.entries(CUSTOMER_DATASETS).map(([cid, info]) => {
          const isSelected = profile.customer_id === cid;
          const hasProducts = info.products.length > 0;

          return (
            <div
              key={cid}
              onClick={() => onSelectCustomer(cid)}
              style={{
                padding: '0.85rem',
                borderRadius: '12px',
                background: isSelected ? 'rgba(99, 102, 241, 0.2)' : 'rgba(30, 41, 59, 0.4)',
                border: isSelected ? '1px solid #6366f1' : '1px solid var(--border-glass)',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
                <strong style={{ fontSize: '0.9rem', color: isSelected ? '#a855f7' : '#f8fafc' }}>{cid}</strong>
                {hasProducts ? (
                  <span className="badge badge-emerald" style={{ fontSize: '0.65rem', padding: '0.15rem 0.4rem' }}>
                    <ShoppingBag size={10} /> {info.products.length} Products
                  </span>
                ) : (
                  <span className="badge badge-rose" style={{ fontSize: '0.65rem', padding: '0.15rem 0.4rem' }}>
                    <Lock size={10} /> No Access
                  </span>
                )}
              </div>

              <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
                {info.name}
              </div>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
                {info.products.length > 0 ? (
                  info.products.map(p => (
                    <span key={p} style={{ fontSize: '0.7rem', padding: '0.1rem 0.35rem', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', textTransform: 'capitalize' }}>
                      {p}
                    </span>
                  ))
                ) : (
                  <span style={{ fontSize: '0.7rem', color: '#f43f5e', italic: 'true' }}>
                    0 Purchased Kits
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

import React from 'react';
import { Code, ExternalLink, ShieldCheck, Check } from 'lucide-react';

export const WidgetView: React.FC = () => {
  return (
    <div className="glass-panel" style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', color: '#c084fc', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Code size={24} />
            Funobotz Embeddable Chatbot Widget & Store Integration
          </h2>
          <p style={{ fontSize: '0.9rem', color: '#94a3b8', marginTop: '0.25rem' }}>
            Integration-ready component suitable for embedding directly into the Funobotz Store or learning ecosystem.
          </p>
        </div>

        <a
          href="http://localhost:5173/demo/embed.html"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-primary"
        >
          <ExternalLink size={16} /> Open Standalone Widget Demo (/demo/embed.html)
        </a>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div style={{ background: 'rgba(15,23,42,0.8)', padding: '1.25rem', borderRadius: '12px', border: '1px solid var(--border-glass)' }}>
          <h4 style={{ fontSize: '1rem', color: '#f8fafc', marginBottom: '0.75rem' }}>
            💻 How to Embed into Funobotz Store
          </h4>
          <p style={{ fontSize: '0.85rem', color: '#cbd5e1', marginBottom: '1rem' }}>
            Add this script snippet to any page on store.funobotz.com:
          </p>

          <pre style={{ background: '#020617', padding: '1rem', borderRadius: '8px', fontSize: '0.8rem', color: '#38bdf8', overflowX: 'auto', border: '1px solid var(--border-glass)' }}>
{`<!-- Funobotz STEM Tutor Widget -->
<script src="http://localhost:5173/widget.js"></script>

<funobotz-tutor 
  data-api-url="http://127.0.0.1:8000/api"
  data-customer-id="FZ-HACK-004"
  data-learner-age="10"
  data-character="tiko"
  data-theme="dark">
</funobotz-tutor>`}
          </pre>

          <ul style={{ fontSize: '0.82rem', color: '#94a3b8', marginTop: '1rem', paddingLeft: '1.2rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
            <li>Isolated Shadow DOM architecture prevents CSS pollution with store styling.</li>
            <li>Configurable customer ID attribute automatically verifies backend product entitlements.</li>
            <li>Standardized REST / JSON interface prepared for future Funobotz Store SDK integration.</li>
          </ul>
        </div>

        <div style={{ background: 'rgba(15,23,42,0.8)', padding: '1.25rem', borderRadius: '12px', border: '1px solid var(--border-glass)' }}>
          <h4 style={{ fontSize: '1rem', color: '#f8fafc', marginBottom: '0.75rem' }}>
            🌐 Live Embed Preview (Iframe / Custom Element)
          </h4>
          <iframe
            src="/demo/embed.html"
            style={{ width: '100%', height: '360px', borderRadius: '10px', border: '1px solid var(--border-glass)', background: '#0f172a' }}
            title="Funobotz Store Embed Preview"
          />
        </div>
      </div>
    </div>
  );
};

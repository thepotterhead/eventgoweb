import { LearnerProfile, CustomerInfo, Character, ChatResponseData } from '../types';

const API_BASE = 'http://127.0.0.1:8000/api';

export async function createSession(profile?: Partial<LearnerProfile>) {
  const res = await fetch(`${API_BASE}/session`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile || {})
  });
  if (!res.ok) throw new Error('Failed to initialize session');
  return res.json();
}

export async function fetchCustomerInfo(customerId: string): Promise<CustomerInfo> {
  const res = await fetch(`${API_BASE}/customer/${customerId}`);
  if (!res.ok) throw new Error(`Customer ID ${customerId} not found`);
  return res.json();
}

export async function fetchCharacters(): Promise<Character[]> {
  const res = await fetch(`${API_BASE}/characters`);
  if (!res.ok) throw new Error('Failed to fetch characters');
  return res.json();
}

export async function updateLearnerProfile(sessionId: string, profile: LearnerProfile) {
  const res = await fetch(`${API_BASE}/learner/update?session_id=${sessionId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profile)
  });
  if (!res.ok) throw new Error('Failed to update learner profile');
  return res.json();
}

export async function sendChatMessage(payload: {
  session_id: string;
  message: string;
  customer_id: string;
  learner_profile?: LearnerProfile;
  requested_character?: string;
}): Promise<ChatResponseData> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}

export async function submitLearningCheck(payload: {
  session_id: string;
  question: string;
  selected_option: number;
  correct_option: number;
}) {
  const res = await fetch(`${API_BASE}/learning-check`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to submit learning check');
  return res.json();
}

export async function triggerDemoScenario(scenarioId: number) {
  const res = await fetch(`${API_BASE}/demo/scenario`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scenario_id: scenarioId })
  });
  if (!res.ok) throw new Error(`Failed to execute scenario ${scenarioId}`);
  return res.json();
}

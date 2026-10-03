export interface LearnerProfile {
  learner_id: string;
  name: string;
  age: number;
  interest: string;
  starting_knowledge: 'Beginner' | 'Intermediate' | 'Advanced';
  current_level: number;
  current_topic: string;
  active_character: string;
  customer_id: string;
}

export interface Character {
  id: string;
  name: string;
  status: 'mapped' | 'behaviour_only' | 'pending';
  avatar: string;
  tagline: string;
  official_context: string;
  verified_facts: string[];
  stem_concepts: string[];
}

export interface CustomerInfo {
  customer_id: string;
  customer_name: string;
  purchased_products: string[];
  accessible_characters: string[];
}

export interface ChatMessage {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: string;
  concept?: string;
  difficulty?: string;
  options?: string[];
  correctOption?: number;
  nextStep?: string;
  accessGranted?: boolean;
  accessNotice?: string;
  unsupportedNotice?: string;
  escalationTriggered?: boolean;
  clarificationNeeded?: boolean;
  clarificationOptions?: string[];
}

export interface ChatResponseData {
  session_id: string;
  answer: string;
  concept: string;
  difficulty: string;
  check_question?: string;
  options?: string[];
  correct_option?: number;
  next_step?: string;
  active_character: string;
  active_topic: string;
  access_granted: boolean;
  access_notice?: string;
  escalation_triggered?: boolean;
  clarification_needed?: boolean;
  clarification_options?: string[];
  unsupported_fact_notice?: string;
}

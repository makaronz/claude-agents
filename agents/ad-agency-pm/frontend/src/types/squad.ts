export type SpecialistType = 
  | 'account-manager'
  | 'creative-director'
  | 'art-director'
  | 'copywriter'
  | 'strategy-planner'
  | 'production-manager';

export interface Specialist {
  id: SpecialistType;
  name: string;
  role: string;
  icon: string;
  color: string;
  description: string;
}

export interface SpecialistResult {
  specialist: SpecialistType;
  analysis: string;
  recommendations: string[];
  insights: string[];
  completedAt: string;
}

export interface SquadAnalysisRequest {
  brief: string;
  projectContext?: {
    budget?: number;
    timeline?: string;
    targetAudience?: string;
    objectives?: string[];
  };
}

export interface SquadAnalysisResponse {
  briefId: string;
  status: 'started' | 'in-progress' | 'completed' | 'failed';
  results: SpecialistResult[];
  synthesis?: string;
  actionPlan?: string[];
  createdAt: string;
  completedAt?: string;
}

export interface SquadAnalysisProgress {
  briefId: string;
  specialist: SpecialistType;
  progress: number; // 0-100
  status: 'pending' | 'analyzing' | 'completed' | 'failed';
  message?: string;
}

export interface SquadSynthesis {
  briefId: string;
  synthesis: string;
  score: number; // 1-10
  strengths: string[];
  weaknesses: string[];
  actionPlan: string[];
  recommendations: string[];
  createdAt: string;
}

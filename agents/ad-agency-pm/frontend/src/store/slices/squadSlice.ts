import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import {
  SpecialistType,
  SpecialistResult,
  SquadAnalysisProgress,
  SquadSynthesis,
} from '@/types/squad';

interface SquadState {
  isSquadMode: boolean;
  currentAnalysis: {
    briefId: string | null;
    brief: string;
    status: 'idle' | 'analyzing' | 'completed' | 'failed';
    progress: Record<SpecialistType, number>;
    results: SpecialistResult[];
    synthesis: SquadSynthesis | null;
  };
  analysisHistory: Array<{
    briefId: string;
    brief: string;
    completedAt: string;
    synthesis: SquadSynthesis;
  }>;
  loading: boolean;
  error: string | null;
}

const initialState: SquadState = {
  isSquadMode: false,
  currentAnalysis: {
    briefId: null,
    brief: '',
    status: 'idle',
    progress: {
      'account-manager': 0,
      'creative-director': 0,
      'art-director': 0,
      'copywriter': 0,
      'strategy-planner': 0,
      'production-manager': 0,
    },
    results: [],
    synthesis: null,
  },
  analysisHistory: [],
  loading: false,
  error: null,
};

const squadSlice = createSlice({
  name: 'squad',
  initialState,
  reducers: {
    toggleSquadMode: (state) => {
      state.isSquadMode = !state.isSquadMode;
    },
    setSquadMode: (state, action: PayloadAction<boolean>) => {
      state.isSquadMode = action.payload;
    },
    startAnalysis: (state, action: PayloadAction<{ briefId: string; brief: string }>) => {
      state.currentAnalysis = {
        ...initialState.currentAnalysis,
        briefId: action.payload.briefId,
        brief: action.payload.brief,
        status: 'analyzing',
      };
    },
    setSquadAnalysisProgress: (state, action: PayloadAction<SquadAnalysisProgress>) => {
      const { specialist, progress } = action.payload;
      state.currentAnalysis.progress[specialist] = progress;
    },
    addSpecialistResult: (state, action: PayloadAction<SpecialistResult>) => {
      state.currentAnalysis.results.push(action.payload);
    },
    setSquadResults: (
      state,
      action: PayloadAction<{ briefId: string; results: SpecialistResult[] }>
    ) => {
      if (state.currentAnalysis.briefId === action.payload.briefId) {
        state.currentAnalysis.results = action.payload.results;
      }
    },
    setSquadSynthesis: (
      state,
      action: PayloadAction<{ briefId: string; synthesis: SquadSynthesis }>
    ) => {
      if (state.currentAnalysis.briefId === action.payload.briefId) {
        state.currentAnalysis.synthesis = action.payload.synthesis;
        state.currentAnalysis.status = 'completed';

        // Add to history
        state.analysisHistory.unshift({
          briefId: action.payload.briefId,
          brief: state.currentAnalysis.brief,
          completedAt: action.payload.synthesis.createdAt,
          synthesis: action.payload.synthesis,
        });
      }
    },
    setAnalysisStatus: (
      state,
      action: PayloadAction<'idle' | 'analyzing' | 'completed' | 'failed'>
    ) => {
      state.currentAnalysis.status = action.payload;
    },
    resetCurrentAnalysis: (state) => {
      state.currentAnalysis = initialState.currentAnalysis;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      if (action.payload) {
        state.currentAnalysis.status = 'failed';
      }
    },
  },
});

export const {
  toggleSquadMode,
  setSquadMode,
  startAnalysis,
  setSquadAnalysisProgress,
  addSpecialistResult,
  setSquadResults,
  setSquadSynthesis,
  setAnalysisStatus,
  resetCurrentAnalysis,
  setLoading,
  setError,
} = squadSlice.actions;

export default squadSlice.reducer;


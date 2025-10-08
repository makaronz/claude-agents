import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import type { SpecialistType, SpecialistResult, SquadAnalysisProgress, SquadSynthesis } from '@/types/squad';

// Types
interface SquadState {
  isSquadMode: boolean;
  currentAnalysis: {
    isRunning: boolean;
    progress: SquadAnalysisProgress | null;
    results: SpecialistResult[];
    synthesis: SquadSynthesis | null;
  };
  error: string | null;
}

type SquadAction =
  | { type: 'TOGGLE_SQUAD_MODE' }
  | { type: 'START_ANALYSIS' }
  | { type: 'UPDATE_PROGRESS'; payload: SquadAnalysisProgress }
  | { type: 'ADD_RESULT'; payload: SpecialistResult }
  | { type: 'SET_SYNTHESIS'; payload: SquadSynthesis }
  | { type: 'RESET_ANALYSIS' }
  | { type: 'SET_ERROR'; payload: string | null };

interface SquadContextType {
  state: SquadState;
  dispatch: React.Dispatch<SquadAction>;
  // Actions
  toggleSquadMode: () => void;
  startAnalysis: () => void;
  updateProgress: (progress: SquadAnalysisProgress) => void;
  addResult: (result: SpecialistResult) => void;
  setSynthesis: (synthesis: SquadSynthesis) => void;
  resetAnalysis: () => void;
  setError: (error: string | null) => void;
}

// Initial state
const initialState: SquadState = {
  isSquadMode: false,
  currentAnalysis: {
    isRunning: false,
    progress: null,
    results: [],
    synthesis: null,
  },
  error: null,
};

// Reducer
const squadReducer = (state: SquadState, action: SquadAction): SquadState => {
  switch (action.type) {
    case 'TOGGLE_SQUAD_MODE':
      return { ...state, isSquadMode: !state.isSquadMode };
    case 'START_ANALYSIS':
      return {
        ...state,
        currentAnalysis: {
          isRunning: true,
          progress: null,
          results: [],
          synthesis: null,
        },
        error: null,
      };
    case 'UPDATE_PROGRESS':
      return {
        ...state,
        currentAnalysis: {
          ...state.currentAnalysis,
          progress: action.payload,
        },
      };
    case 'ADD_RESULT':
      return {
        ...state,
        currentAnalysis: {
          ...state.currentAnalysis,
          results: [...state.currentAnalysis.results, action.payload],
        },
      };
    case 'SET_SYNTHESIS':
      return {
        ...state,
        currentAnalysis: {
          ...state.currentAnalysis,
          isRunning: false,
          synthesis: action.payload,
        },
      };
    case 'RESET_ANALYSIS':
      return {
        ...state,
        currentAnalysis: {
          isRunning: false,
          progress: null,
          results: [],
          synthesis: null,
        },
        error: null,
      };
    case 'SET_ERROR':
      return {
        ...state,
        error: action.payload,
        currentAnalysis: {
          ...state.currentAnalysis,
          isRunning: false,
        },
      };
    default:
      return state;
  }
};

// Context
const SquadContext = createContext<SquadContextType | undefined>(undefined);

// Provider
export const SquadProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(squadReducer, initialState);

  // Action creators
  const toggleSquadMode = () => dispatch({ type: 'TOGGLE_SQUAD_MODE' });
  const startAnalysis = () => dispatch({ type: 'START_ANALYSIS' });
  const updateProgress = (progress: SquadAnalysisProgress) => dispatch({ type: 'UPDATE_PROGRESS', payload: progress });
  const addResult = (result: SpecialistResult) => dispatch({ type: 'ADD_RESULT', payload: result });
  const setSynthesis = (synthesis: SquadSynthesis) => dispatch({ type: 'SET_SYNTHESIS', payload: synthesis });
  const resetAnalysis = () => dispatch({ type: 'RESET_ANALYSIS' });
  const setError = (error: string | null) => dispatch({ type: 'SET_ERROR', payload: error });

  const value: SquadContextType = {
    state,
    dispatch,
    toggleSquadMode,
    startAnalysis,
    updateProgress,
    addResult,
    setSynthesis,
    resetAnalysis,
    setError,
  };

  return <SquadContext.Provider value={value}>{children}</SquadContext.Provider>;
};

// Hook
export const useSquadContext = (): SquadContextType => {
  const context = useContext(SquadContext);
  if (context === undefined) {
    throw new Error('useSquadContext must be used within a SquadProvider');
  }
  return context;
};

// Selectors
export const useSquadMode = () => {
  const { state } = useSquadContext();
  return state.isSquadMode;
};

export const useSquadAnalysis = () => {
  const { state } = useSquadContext();
  return state.currentAnalysis;
};

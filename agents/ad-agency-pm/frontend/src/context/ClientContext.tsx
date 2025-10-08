import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import type { Client } from '@/types/client';

// Types
interface ClientState {
  clients: Client[];
  loading: boolean;
  error: string | null;
}

type ClientAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_CLIENTS'; payload: Client[] }
  | { type: 'ADD_CLIENT'; payload: Client }
  | { type: 'UPDATE_CLIENT'; payload: Client }
  | { type: 'DELETE_CLIENT'; payload: string };

interface ClientContextType {
  state: ClientState;
  dispatch: React.Dispatch<ClientAction>;
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setClients: (clients: Client[]) => void;
  addClient: (client: Client) => void;
  updateClient: (client: Client) => void;
  deleteClient: (id: string) => void;
}

// Initial state
const initialState: ClientState = {
  clients: [],
  loading: false,
  error: null,
};

// Reducer
const clientReducer = (state: ClientState, action: ClientAction): ClientState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_CLIENTS':
      return { ...state, clients: action.payload, loading: false };
    case 'ADD_CLIENT':
      return { ...state, clients: [...state.clients, action.payload] };
    case 'UPDATE_CLIENT':
      return {
        ...state,
        clients: state.clients.map(c => c.id === action.payload.id ? action.payload : c),
      };
    case 'DELETE_CLIENT':
      return {
        ...state,
        clients: state.clients.filter(c => c.id !== action.payload),
      };
    default:
      return state;
  }
};

// Context
const ClientContext = createContext<ClientContextType | undefined>(undefined);

// Provider
export const ClientProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(clientReducer, {
    ...initialState,
    clients: [
      {
        id: 'client-1',
        name: 'Nike Inc.',
        email: 'contact@nike.com',
        phone: '+1-555-0123',
        company: 'Nike Inc.',
        industry: 'Sports & Fashion',
        budgetRange: '$100k-$500k',
        notes: 'Major sports brand, seasonal campaigns',
        activeProjects: 2,
        lastContact: '2024-01-15',
        createdAt: '2024-01-01',
        updatedAt: '2024-01-15',
      },
      {
        id: 'client-2',
        name: 'Apple Inc.',
        email: 'marketing@apple.com',
        phone: '+1-555-0456',
        company: 'Apple Inc.',
        industry: 'Technology',
        budgetRange: '$500k+',
        notes: 'Premium brand, high-quality requirements',
        activeProjects: 1,
        lastContact: '2024-02-01',
        createdAt: '2024-01-15',
        updatedAt: '2024-02-01',
      },
      {
        id: 'client-3',
        name: 'Local Startup',
        email: 'founder@localstartup.com',
        phone: '+1-555-0789',
        company: 'Local Startup Co.',
        industry: 'SaaS',
        budgetRange: '$10k-$50k',
        notes: 'Early-stage company, budget-conscious',
        activeProjects: 0,
        lastContact: '2024-01-20',
        createdAt: '2024-01-10',
        updatedAt: '2024-01-20',
      },
    ],
  });

  // Action creators
  const setLoading = (loading: boolean) => dispatch({ type: 'SET_LOADING', payload: loading });
  const setError = (error: string | null) => dispatch({ type: 'SET_ERROR', payload: error });
  const setClients = (clients: Client[]) => dispatch({ type: 'SET_CLIENTS', payload: clients });
  const addClient = (client: Client) => dispatch({ type: 'ADD_CLIENT', payload: client });
  const updateClient = (client: Client) => dispatch({ type: 'UPDATE_CLIENT', payload: client });
  const deleteClient = (id: string) => dispatch({ type: 'DELETE_CLIENT', payload: id });

  const value: ClientContextType = {
    state,
    dispatch,
    setLoading,
    setError,
    setClients,
    addClient,
    updateClient,
    deleteClient,
  };

  return <ClientContext.Provider value={value}>{children}</ClientContext.Provider>;
};

// Hook
export const useClientContext = (): ClientContextType => {
  const context = useContext(ClientContext);
  if (context === undefined) {
    throw new Error('useClientContext must be used within a ClientProvider');
  }
  return context;
};

// Selectors
export const useClients = () => {
  const { state } = useClientContext();
  return state.clients;
};

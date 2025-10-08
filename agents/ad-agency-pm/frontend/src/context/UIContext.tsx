import React, { createContext, useContext, useReducer, ReactNode } from 'react';

// Types
interface UIState {
  sidebarOpen: boolean;
  notifications: Array<{
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    message: string;
    timestamp: number;
  }>;
}

type UIAction =
  | { type: 'TOGGLE_SIDEBAR' }
  | { type: 'SET_SIDEBAR_OPEN'; payload: boolean }
  | { type: 'ADD_NOTIFICATION'; payload: Omit<UIState['notifications'][0], 'id' | 'timestamp'> }
  | { type: 'REMOVE_NOTIFICATION'; payload: string }
  | { type: 'CLEAR_NOTIFICATIONS' };

interface UIContextType {
  state: UIState;
  dispatch: React.Dispatch<UIAction>;
  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  addNotification: (notification: Omit<UIState['notifications'][0], 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

// Initial state
const initialState: UIState = {
  sidebarOpen: true,
  notifications: [],
};

// Reducer
const uiReducer = (state: UIState, action: UIAction): UIState => {
  switch (action.type) {
    case 'TOGGLE_SIDEBAR':
      return { ...state, sidebarOpen: !state.sidebarOpen };
    case 'SET_SIDEBAR_OPEN':
      return { ...state, sidebarOpen: action.payload };
    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [
          ...state.notifications,
          {
            ...action.payload,
            id: Math.random().toString(36).substr(2, 9),
            timestamp: Date.now(),
          },
        ],
      };
    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload),
      };
    case 'CLEAR_NOTIFICATIONS':
      return { ...state, notifications: [] };
    default:
      return state;
  }
};

// Context
const UIContext = createContext<UIContextType | undefined>(undefined);

// Provider
export const UIProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(uiReducer, initialState);

  // Action creators
  const toggleSidebar = () => dispatch({ type: 'TOGGLE_SIDEBAR' });
  const setSidebarOpen = (open: boolean) => dispatch({ type: 'SET_SIDEBAR_OPEN', payload: open });
  const addNotification = (notification: Omit<UIState['notifications'][0], 'id' | 'timestamp'>) =>
    dispatch({ type: 'ADD_NOTIFICATION', payload: notification });
  const removeNotification = (id: string) => dispatch({ type: 'REMOVE_NOTIFICATION', payload: id });
  const clearNotifications = () => dispatch({ type: 'CLEAR_NOTIFICATIONS' });

  const value: UIContextType = {
    state,
    dispatch,
    toggleSidebar,
    setSidebarOpen,
    addNotification,
    removeNotification,
    clearNotifications,
  };

  return <UIContext.Provider value={value}>{children}</UIContext.Provider>;
};

// Hook
export const useUIContext = (): UIContextType => {
  const context = useContext(UIContext);
  if (context === undefined) {
    throw new Error('useUIContext must be used within a UIProvider');
  }
  return context;
};

// Selectors
export const useSidebar = () => {
  const { state, toggleSidebar, setSidebarOpen } = useUIContext();
  return {
    isOpen: state.sidebarOpen,
    toggle: toggleSidebar,
    setOpen: setSidebarOpen,
  };
};

export const useNotifications = () => {
  const { state, addNotification, removeNotification, clearNotifications } = useUIContext();
  return {
    notifications: state.notifications,
    add: addNotification,
    remove: removeNotification,
    clear: clearNotifications,
  };
};

import React, { createContext, useContext, useReducer, ReactNode, useCallback, useMemo, useEffect, useRef } from 'react';
import type { Project, ProjectStatus, Priority, Task, CreateProjectRequest, UpdateProjectRequest } from '@/types/project';

// Types
interface ProjectState {
  projects: Project[];
  selectedProject: Project | null;
  loading: boolean;
  error: string | null;
  filters: {
    status: ProjectStatus | null;
    priority: Priority | null;
    search: string;
  };
}

type ProjectAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_PROJECTS'; payload: Project[] }
  | { type: 'ADD_PROJECT'; payload: Project }
  | { type: 'UPDATE_PROJECT'; payload: Project }
  | { type: 'DELETE_PROJECT'; payload: string }
  | { type: 'SELECT_PROJECT'; payload: Project | null }
  | { type: 'SET_FILTERS'; payload: Partial<ProjectState['filters']> }
  | { type: 'RESET_FILTERS' };

interface ProjectContextType {
  state: ProjectState;
  dispatch: React.Dispatch<ProjectAction>;
  // Actions
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  setProjects: (projects: Project[]) => void;
  addProject: (project: Project) => void;
  updateProject: (project: Project) => void;
  deleteProject: (id: string) => void;
  selectProject: (project: Project | null) => void;
  setFilters: (filters: Partial<ProjectState['filters']>) => void;
  resetFilters: () => void;
}

// Initial state
const initialState: ProjectState = {
  projects: [],
  selectedProject: null,
  loading: false,
  error: null,
  filters: {
    status: null,
    priority: null,
    search: '',
  },
};

// Reducer
const projectReducer = (state: ProjectState, action: ProjectAction): ProjectState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_PROJECTS':
      return { ...state, projects: action.payload, loading: false };
    case 'ADD_PROJECT':
      return { ...state, projects: [...state.projects, action.payload] };
    case 'UPDATE_PROJECT':
      return {
        ...state,
        projects: state.projects.map(p => p.id === action.payload.id ? action.payload : p),
        selectedProject: state.selectedProject?.id === action.payload.id ? action.payload : state.selectedProject,
      };
    case 'DELETE_PROJECT':
      return {
        ...state,
        projects: state.projects.filter(p => p.id !== action.payload),
        selectedProject: state.selectedProject?.id === action.payload ? null : state.selectedProject,
      };
    case 'SELECT_PROJECT':
      return { ...state, selectedProject: action.payload };
    case 'SET_FILTERS':
      return { ...state, filters: { ...state.filters, ...action.payload } };
    case 'RESET_FILTERS':
      return { ...state, filters: { status: null, priority: null, search: '' } };
    default:
      return state;
  }
};

// Context
const ProjectContext = createContext<ProjectContextType | undefined>(undefined);

// Provider
export const ProjectProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(projectReducer, initialState);
  const projectsLoaded = useRef(false);

  // Load initial mock data
  useEffect(() => {
    if (!projectsLoaded.current) {
      projectsLoaded.current = true;
      dispatch({ type: 'SET_LOADING', payload: true });
      
      // Mock data - replace with actual API call
      const mockProjects: Project[] = [
        {
          id: '1',
          name: 'Nike Campaign',
          description: 'Summer 2024 sneaker launch campaign',
          clientId: 'client-1',
          clientName: 'Nike Inc.',
          status: 'In Progress',
          priority: 'High',
          progress: 75,
          budget: 250000,
          deadline: '2024-06-15',
          teamMembers: [
            { id: 'creative-director', name: 'John Doe', role: 'Creative Director' },
            { id: 'copywriter', name: 'Jane Smith', role: 'Copywriter' },
            { id: 'art-director', name: 'Peter Jones', role: 'Art Director' }
          ],
          createdAt: '2024-01-15',
          updatedAt: '2024-02-10',
        },
        {
          id: '2',
          name: 'Apple Watch Ad',
          description: 'New Apple Watch Series 10 advertisement',
          clientId: 'client-2',
          clientName: 'Apple Inc.',
          status: 'Planning',
          priority: 'Medium',
          progress: 25,
          budget: 180000,
          deadline: '2024-07-01',
          teamMembers: [
            { id: 'creative-director', name: 'John Doe', role: 'Creative Director' },
            { id: 'production-manager', name: 'Alice Brown', role: 'Production Manager' }
          ],
          createdAt: '2024-02-01',
          updatedAt: '2024-02-05',
        },
      ];
      
      // Simulate API delay
      setTimeout(() => {
        dispatch({ type: 'SET_PROJECTS', payload: mockProjects });
      }, 1000);
    }
  }, []); // Empty dependency array - run only once on mount

  // Action creators - simplified without useCallback
  const setLoading = (loading: boolean) => dispatch({ type: 'SET_LOADING', payload: loading });
  const setError = (error: string | null) => dispatch({ type: 'SET_ERROR', payload: error });
  const setProjects = (projects: Project[]) => dispatch({ type: 'SET_PROJECTS', payload: projects });
  const addProject = (project: Project) => dispatch({ type: 'ADD_PROJECT', payload: project });
  const updateProject = (project: Project) => dispatch({ type: 'UPDATE_PROJECT', payload: project });
  const deleteProject = (id: string) => dispatch({ type: 'DELETE_PROJECT', payload: id });
  const selectProject = (project: Project | null) => dispatch({ type: 'SELECT_PROJECT', payload: project });
  const setFilters = (filters: Partial<ProjectState['filters']>) => dispatch({ type: 'SET_FILTERS', payload: filters });
  const resetFilters = () => dispatch({ type: 'RESET_FILTERS' });

  // Use ref to store stable value
  const valueRef = useRef<ProjectContextType>();
  
  if (!valueRef.current) {
    valueRef.current = {
      state,
      dispatch,
      setLoading,
      setError,
      setProjects,
      addProject,
      updateProject,
      deleteProject,
      selectProject,
      setFilters,
      resetFilters,
    };
  } else {
    // Update only the state part
    valueRef.current.state = state;
  }

  return <ProjectContext.Provider value={valueRef.current}>{children}</ProjectContext.Provider>;
};

// Hook
export const useProjectContext = (): ProjectContextType => {
  const context = useContext(ProjectContext);
  if (context === undefined) {
    throw new Error('useProjectContext must be used within a ProjectProvider');
  }
  return context;
};

// Selectors
export const useProjects = () => {
  const { state } = useProjectContext();
  return state.projects;
};

export const useSelectedProject = () => {
  const { state } = useProjectContext();
  return state.selectedProject;
};

export const useProjectFilters = () => {
  const { state } = useProjectContext();
  return state.filters;
};

export const useFilteredProjects = () => {
  const { state } = useProjectContext();
  const { projects, filters } = state;

  return useMemo(() => {
    return projects.filter(project => {
      if (filters.status && project.status !== filters.status) return false;
      if (filters.priority && project.priority !== filters.priority) return false;
      if (filters.search && !project.name.toLowerCase().includes(filters.search.toLowerCase())) return false;
      return true;
    });
  }, [projects, filters.status, filters.priority, filters.search]);
};

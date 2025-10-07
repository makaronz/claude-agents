# 🚀 Frontend Implementation Guide

## 📋 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Basic knowledge of React, TypeScript, and modern web development
- Understanding of REST APIs and WebSockets

### Project Setup

```bash
# Create new React project with TypeScript
npx create-react-app ad-agency-pm-frontend --template typescript
cd ad-agency-pm-frontend

# Install additional dependencies
npm install @reduxjs/toolkit react-redux
npm install @tanstack/react-query
npm install socket.io-client
npm install react-router-dom
npm install @headlessui/react @heroicons/react
npm install react-hook-form @hookform/resolvers zod
npm install recharts
npm install @dnd-kit/core @dnd-kit/sortable
npm install tailwindcss @tailwindcss/forms

# Development dependencies
npm install -D @types/node
npm install -D eslint @typescript-eslint/eslint-plugin
npm install -D prettier
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D playwright
```

## 🏗️ Project Structure Setup

```
src/
├── components/
│   ├── common/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   └── index.ts
│   │   ├── Card/
│   │   ├── Modal/
│   │   ├── Input/
│   │   └── Loading/
│   ├── layout/
│   │   ├── Header/
│   │   ├── Sidebar/
│   │   └── Navigation/
│   ├── dashboard/
│   │   ├── StatsCards/
│   │   ├── QuickActions/
│   │   └── UpcomingDeadlines/
│   ├── projects/
│   │   ├── ProjectList/
│   │   ├── ProjectCard/
│   │   └── TaskBoard/
│   ├── squad/
│   │   ├── SquadModeToggle/
│   │   ├── BriefInput/
│   │   └── SpecialistCards/
│   └── clients/
│       ├── ClientList/
│       └── ClientCard/
├── pages/
│   ├── Dashboard/
│   ├── Projects/
│   ├── Clients/
│   └── Squad/
├── hooks/
│   ├── useWebSocket.ts
│   ├── useProjects.ts
│   └── useSquad.ts
├── store/
│   ├── index.ts
│   ├── slices/
│   │   ├── projectsSlice.ts
│   │   ├── clientsSlice.ts
│   │   └── squadSlice.ts
│   └── api/
│       ├── projectsApi.ts
│       ├── clientsApi.ts
│       └── squadApi.ts
├── types/
│   ├── project.ts
│   ├── client.ts
│   └── squad.ts
├── utils/
│   ├── api.ts
│   ├── validation.ts
│   └── helpers.ts
└── App.tsx
```

## 🎨 Core Components Implementation

### 1. Button Component

```typescript
// src/components/common/Button/Button.tsx
import React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/utils/helpers';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-primary',
        squad: 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700 shadow-lg',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, loading, children, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg
            className="mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button, buttonVariants };
```

### 2. Card Component

```typescript
// src/components/common/Card/Card.tsx
import React from 'react';
import { cn } from '@/utils/helpers';

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    variant?: 'default' | 'squad' | 'elevated';
  }
>(({ className, variant = 'default', ...props }, ref) => {
  const variants = {
    default: 'bg-white border border-gray-200 shadow-sm',
    squad: 'bg-gradient-to-br from-purple-50 to-blue-50 border-2 border-purple-200 shadow-lg',
    elevated: 'bg-white border border-gray-200 shadow-lg hover:shadow-xl transition-shadow',
  };

  return (
    <div
      ref={ref}
      className={cn(
        'rounded-lg p-6 transition-all duration-200',
        variants[variant],
        className
      )}
      {...props}
    />
  );
});

Card.displayName = 'Card';

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 pb-4', className)}
    {...props}
  />
));

CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn('text-lg font-semibold leading-none tracking-tight', className)}
    {...props}
  />
));

CardTitle.displayName = 'CardTitle';

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('pt-0', className)} {...props} />
));

CardContent.displayName = 'CardContent';

export { Card, CardHeader, CardTitle, CardContent };
```

### 3. Project Card Component

```typescript
// src/components/projects/ProjectCard/ProjectCard.tsx
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { Project } from '@/types/project';
import { cn } from '@/utils/helpers';

interface ProjectCardProps {
  project: Project;
  onEdit?: (project: Project) => void;
  onView?: (project: Project) => void;
  className?: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({
  project,
  onEdit,
  onView,
  className,
}) => {
  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in progress':
        return 'bg-blue-100 text-blue-800';
      case 'on hold':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'critical':
        return 'text-red-600';
      case 'high':
        return 'text-orange-600';
      case 'medium':
        return 'text-yellow-600';
      case 'low':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <Card className={cn('hover:shadow-lg transition-shadow cursor-pointer', className)}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg font-semibold text-gray-900">
              {project.name}
            </CardTitle>
            <p className="text-sm text-gray-600 mt-1">{project.clientName}</p>
          </div>
          <div className="flex items-center space-x-2">
            <span
              className={cn(
                'px-2 py-1 rounded-full text-xs font-medium',
                getStatusColor(project.status)
              )}
            >
              {project.status}
            </span>
            <span className={cn('text-xs font-medium', getPriorityColor(project.priority))}>
              {project.priority}
            </span>
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <p className="text-sm text-gray-700 mb-4 line-clamp-2">
          {project.description}
        </p>
        
        <div className="space-y-3">
          {/* Progress Bar */}
          <div>
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Progress</span>
              <span>{project.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${project.progress}%` }}
              />
            </div>
          </div>
          
          {/* Project Details */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Budget:</span>
              <span className="ml-1 font-medium">${project.budget.toLocaleString()}</span>
            </div>
            <div>
              <span className="text-gray-500">Due:</span>
              <span className="ml-1 font-medium">
                {new Date(project.deadline).toLocaleDateString()}
              </span>
            </div>
          </div>
          
          {/* Team Members */}
          <div>
            <span className="text-sm text-gray-500">Team:</span>
            <div className="flex -space-x-2 mt-1">
              {project.teamMembers.slice(0, 4).map((member, index) => (
                <div
                  key={index}
                  className="w-8 h-8 rounded-full bg-gray-300 border-2 border-white flex items-center justify-center text-xs font-medium text-gray-700"
                >
                  {member.name.charAt(0).toUpperCase()}
                </div>
              ))}
              {project.teamMembers.length > 4 && (
                <div className="w-8 h-8 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-xs font-medium text-gray-600">
                  +{project.teamMembers.length - 4}
                </div>
              )}
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="flex space-x-2 pt-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onView?.(project)}
              className="flex-1"
            >
              View
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onEdit?.(project)}
              className="flex-1"
            >
              Edit
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProjectCard;
```

### 4. Squad Mode Toggle Component

```typescript
// src/components/squad/SquadModeToggle/SquadModeToggle.tsx
import React from 'react';
import { Button } from '@/components/common/Button';
import { cn } from '@/utils/helpers';

interface SquadModeToggleProps {
  isSquadMode: boolean;
  onToggle: (enabled: boolean) => void;
  specialistCount?: number;
  className?: string;
}

const SquadModeToggle: React.FC<SquadModeToggleProps> = ({
  isSquadMode,
  onToggle,
  specialistCount = 6,
  className,
}) => {
  return (
    <div className={cn('flex items-center space-x-4', className)}>
      <div className="flex items-center space-x-2">
        <span className="text-sm font-medium text-gray-700">Solo Mode</span>
        <button
          onClick={() => onToggle(!isSquadMode)}
          className={cn(
            'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
            isSquadMode ? 'bg-gradient-to-r from-purple-600 to-blue-600' : 'bg-gray-200'
          )}
        >
          <span
            className={cn(
              'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
              isSquadMode ? 'translate-x-6' : 'translate-x-1'
            )}
          />
        </button>
        <span className="text-sm font-medium text-gray-700">Squad Mode</span>
      </div>
      
      {isSquadMode && (
        <div className="flex items-center space-x-2 text-sm text-purple-600">
          <div className="flex -space-x-1">
            {Array.from({ length: specialistCount }).map((_, index) => (
              <div
                key={index}
                className="w-6 h-6 rounded-full bg-gradient-to-r from-purple-500 to-blue-500 border-2 border-white flex items-center justify-center text-xs font-bold text-white"
              >
                {index + 1}
              </div>
            ))}
          </div>
          <span className="font-medium">{specialistCount} Specialists Ready</span>
        </div>
      )}
    </div>
  );
};

export default SquadModeToggle;
```

## 🔌 State Management Setup

### 1. Redux Store Configuration

```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import { projectsApi } from './api/projectsApi';
import { clientsApi } from './api/clientsApi';
import { squadApi } from './api/squadApi';
import projectsSlice from './slices/projectsSlice';
import clientsSlice from './slices/clientsSlice';
import squadSlice from './slices/squadSlice';
import uiSlice from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    projects: projectsSlice,
    clients: clientsSlice,
    squad: squadSlice,
    ui: uiSlice,
    [projectsApi.reducerPath]: projectsApi.reducer,
    [clientsApi.reducerPath]: clientsApi.reducer,
    [squadApi.reducerPath]: squadApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(projectsApi.middleware)
      .concat(clientsApi.middleware)
      .concat(squadApi.middleware),
});

setupListeners(store.dispatch);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 2. Projects Slice

```typescript
// src/store/slices/projectsSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Project } from '@/types/project';

interface ProjectsState {
  projects: Project[];
  selectedProject: Project | null;
  loading: boolean;
  error: string | null;
  filters: {
    status: string[];
    priority: string[];
    client: string[];
  };
}

const initialState: ProjectsState = {
  projects: [],
  selectedProject: null,
  loading: false,
  error: null,
  filters: {
    status: [],
    priority: [],
    client: [],
  },
};

const projectsSlice = createSlice({
  name: 'projects',
  initialState,
  reducers: {
    setProjects: (state, action: PayloadAction<Project[]>) => {
      state.projects = action.payload;
    },
    addProject: (state, action: PayloadAction<Project>) => {
      state.projects.push(action.payload);
    },
    updateProject: (state, action: PayloadAction<Project>) => {
      const index = state.projects.findIndex(p => p.id === action.payload.id);
      if (index !== -1) {
        state.projects[index] = action.payload;
      }
    },
    deleteProject: (state, action: PayloadAction<string>) => {
      state.projects = state.projects.filter(p => p.id !== action.payload);
    },
    setSelectedProject: (state, action: PayloadAction<Project | null>) => {
      state.selectedProject = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setFilters: (state, action: PayloadAction<Partial<ProjectsState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
  },
});

export const {
  setProjects,
  addProject,
  updateProject,
  deleteProject,
  setSelectedProject,
  setLoading,
  setError,
  setFilters,
} = projectsSlice.actions;

export default projectsSlice.reducer;
```

### 3. API Integration

```typescript
// src/store/api/projectsApi.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { Project, CreateProjectRequest, UpdateProjectRequest } from '@/types/project';

export const projectsApi = createApi({
  reducerPath: 'projectsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.REACT_APP_API_URL + '/api/projects',
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Project'],
  endpoints: (builder) => ({
    getProjects: builder.query<Project[], void>({
      query: () => '',
      providesTags: ['Project'],
    }),
    getProject: builder.query<Project, string>({
      query: (id) => `/${id}`,
      providesTags: (result, error, id) => [{ type: 'Project', id }],
    }),
    createProject: builder.mutation<Project, CreateProjectRequest>({
      query: (project) => ({
        url: '',
        method: 'POST',
        body: project,
      }),
      invalidatesTags: ['Project'],
    }),
    updateProject: builder.mutation<Project, UpdateProjectRequest>({
      query: ({ id, ...project }) => ({
        url: `/${id}`,
        method: 'PUT',
        body: project,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Project', id }],
    }),
    deleteProject: builder.mutation<void, string>({
      query: (id) => ({
        url: `/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Project'],
    }),
  }),
});

export const {
  useGetProjectsQuery,
  useGetProjectQuery,
  useCreateProjectMutation,
  useUpdateProjectMutation,
  useDeleteProjectMutation,
} = projectsApi;
```

## 🔌 WebSocket Integration

### 1. WebSocket Hook

```typescript
// src/hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { useAppDispatch } from '@/store';
import { addProject, updateProject, deleteProject } from '@/store/slices/projectsSlice';
import { addClient, updateClient } from '@/store/slices/clientsSlice';
import { setSquadAnalysisProgress, setSquadResults } from '@/store/slices/squadSlice';

interface WebSocketEvents {
  'project:created': any;
  'project:updated': any;
  'project:deleted': { id: string };
  'client:created': any;
  'client:updated': any;
  'squad:analysis:progress': { briefId: string; specialist: string; progress: number };
  'squad:analysis:completed': { briefId: string; results: any[] };
  'squad:synthesis:completed': { briefId: string; synthesis: string };
}

export const useWebSocket = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [connected, setConnected] = useState(false);
  const dispatch = useAppDispatch();

  useEffect(() => {
    const newSocket = io(process.env.REACT_APP_WS_URL || 'ws://localhost:8000', {
      transports: ['websocket'],
    });

    newSocket.on('connect', () => {
      setConnected(true);
      console.log('WebSocket connected');
    });

    newSocket.on('disconnect', () => {
      setConnected(false);
      console.log('WebSocket disconnected');
    });

    // Project events
    newSocket.on('project:created', (project) => {
      dispatch(addProject(project));
    });

    newSocket.on('project:updated', (project) => {
      dispatch(updateProject(project));
    });

    newSocket.on('project:deleted', ({ id }) => {
      dispatch(deleteProject(id));
    });

    // Client events
    newSocket.on('client:created', (client) => {
      dispatch(addClient(client));
    });

    newSocket.on('client:updated', (client) => {
      dispatch(updateClient(client));
    });

    // Squad events
    newSocket.on('squad:analysis:progress', ({ briefId, specialist, progress }) => {
      dispatch(setSquadAnalysisProgress({ briefId, specialist, progress }));
    });

    newSocket.on('squad:analysis:completed', ({ briefId, results }) => {
      dispatch(setSquadResults({ briefId, results }));
    });

    newSocket.on('squad:synthesis:completed', ({ briefId, synthesis }) => {
      dispatch(setSquadSynthesis({ briefId, synthesis }));
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [dispatch]);

  const emit = <K extends keyof WebSocketEvents>(
    event: K,
    data: WebSocketEvents[K]
  ) => {
    if (socket) {
      socket.emit(event, data);
    }
  };

  return { socket, connected, emit };
};
```

### 2. Squad Analysis Component

```typescript
// src/components/squad/SquadAnalysis/SquadAnalysis.tsx
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useSquadAnalysisMutation } from '@/store/api/squadApi';

interface Specialist {
  id: string;
  name: string;
  role: string;
  icon: string;
  color: string;
}

const SPECIALISTS: Specialist[] = [
  { id: 'account-manager', name: 'Account Manager', role: 'Brief Analysis', icon: '👔', color: 'bg-blue-500' },
  { id: 'creative-director', name: 'Creative Director', role: 'Strategy & Vision', icon: '🎨', color: 'bg-purple-500' },
  { id: 'art-director', name: 'Art Director', role: 'Visual Concepts', icon: '🎯', color: 'bg-green-500' },
  { id: 'copywriter', name: 'Copywriter', role: 'Messaging', icon: '✍️', color: 'bg-orange-500' },
  { id: 'strategy-planner', name: 'Strategy Planner', role: 'Media Strategy', icon: '📊', color: 'bg-red-500' },
  { id: 'production-manager', name: 'Production Manager', role: 'Timeline & Resources', icon: '🎬', color: 'bg-indigo-500' },
];

interface SquadAnalysisProps {
  brief: string;
  onAnalysisComplete?: (results: any) => void;
}

const SquadAnalysis: React.FC<SquadAnalysisProps> = ({ brief, onAnalysisComplete }) => {
  const [analysisProgress, setAnalysisProgress] = useState<Record<string, number>>({});
  const [results, setResults] = useState<Record<string, any>>({});
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const { emit } = useWebSocket();
  const [startAnalysis] = useSquadAnalysisMutation();

  const handleStartAnalysis = async () => {
    if (!brief.trim()) return;
    
    setIsAnalyzing(true);
    setAnalysisProgress({});
    setResults({});
    
    try {
      const response = await startAnalysis({ brief }).unwrap();
      emit('squad:analysis:started', { briefId: response.briefId });
    } catch (error) {
      console.error('Failed to start analysis:', error);
      setIsAnalyzing(false);
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress < 30) return 'bg-red-500';
    if (progress < 70) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  const isAnalysisComplete = Object.values(analysisProgress).every(progress => progress === 100);

  useEffect(() => {
    if (isAnalysisComplete && Object.keys(results).length > 0) {
      setIsAnalyzing(false);
      onAnalysisComplete?.(results);
    }
  }, [isAnalysisComplete, results, onAnalysisComplete]);

  return (
    <div className="space-y-6">
      <div className="text-center">
        <Button
          onClick={handleStartAnalysis}
          disabled={!brief.trim() || isAnalyzing}
          variant="squad"
          size="lg"
          loading={isAnalyzing}
        >
          {isAnalyzing ? 'Analyzing...' : '🎭 Start Squad Analysis'}
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {SPECIALISTS.map((specialist) => {
          const progress = analysisProgress[specialist.id] || 0;
          const result = results[specialist.id];
          
          return (
            <Card key={specialist.id} variant="squad">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <span className="text-2xl">{specialist.icon}</span>
                  <div>
                    <div className="text-sm font-medium">{specialist.name}</div>
                    <div className="text-xs text-gray-600">{specialist.role}</div>
                  </div>
                </CardTitle>
              </CardHeader>
              
              <CardContent>
                {isAnalyzing && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Progress</span>
                      <span>{progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-500 ${getProgressColor(progress)}`}
                        style={{ width: `${progress}%` }}
                      />
                    </div>
                  </div>
                )}
                
                {result && (
                  <div className="mt-4">
                    <div className="text-sm font-medium text-green-600 mb-2">
                      ✅ Analysis Complete
                    </div>
                    <div className="text-xs text-gray-700 bg-white p-2 rounded border">
                      {result.summary || 'Analysis completed successfully'}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default SquadAnalysis;
```

## 📱 Responsive Layout

### 1. Main Layout Component

```typescript
// src/components/layout/Layout/Layout.tsx
import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../Header/Header';
import Sidebar from '../Sidebar/Sidebar';
import { cn } from '@/utils/helpers';

const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main content */}
      <div className="lg:pl-64">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
```

### 2. Responsive Sidebar

```typescript
// src/components/layout/Sidebar/Sidebar.tsx
import React from 'react';
import { NavLink } from 'react-router-dom';
import { cn } from '@/utils/helpers';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'Projects', href: '/projects', icon: '📋' },
  { name: 'Clients', href: '/clients', icon: '👥' },
  { name: 'Squad Mode', href: '/squad', icon: '🎭' },
  { name: 'Analytics', href: '/analytics', icon: '📈' },
  { name: 'Settings', href: '/settings', icon: '⚙️' },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  return (
    <div
      className={cn(
        'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0',
        isOpen ? 'translate-x-0' : '-translate-x-full'
      )}
    >
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="flex h-16 items-center justify-center border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-900">🎯 Ad Agency PM</h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-2 py-4">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              onClick={onClose}
              className={({ isActive }) =>
                cn(
                  'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors',
                  isActive
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                )
              }
            >
              <span className="mr-3 text-lg">{item.icon}</span>
              {item.name}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="border-t border-gray-200 p-4">
          <div className="text-xs text-gray-500 text-center">
            Ad Agency Project Manager v1.0.0
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
```

## 🧪 Testing Setup

### 1. Component Testing

```typescript
// src/components/common/Button/Button.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByText('Loading')).toBeInTheDocument();
  });

  it('applies correct variant classes', () => {
    render(<Button variant="squad">Squad Mode</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-gradient-to-r', 'from-purple-600', 'to-blue-600');
  });
});
```

### 2. Integration Testing

```typescript
// src/components/projects/ProjectCard/ProjectCard.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '@/store';
import ProjectCard from './ProjectCard';
import { Project } from '@/types/project';

const mockProject: Project = {
  id: '1',
  name: 'Test Project',
  description: 'Test Description',
  clientName: 'Test Client',
  status: 'In Progress',
  priority: 'High',
  progress: 75,
  budget: 25000,
  deadline: '2025-02-01',
  teamMembers: [
    { id: '1', name: 'John Doe', role: 'Designer' },
    { id: '2', name: 'Jane Smith', role: 'Developer' },
  ],
  createdAt: '2025-01-01',
  updatedAt: '2025-01-10',
};

const renderWithProvider = (component: React.ReactElement) => {
  return render(
    <Provider store={store}>
      {component}
    </Provider>
  );
};

describe('ProjectCard', () => {
  it('renders project information correctly', () => {
    renderWithProvider(<ProjectCard project={mockProject} />);
    
    expect(screen.getByText('Test Project')).toBeInTheDocument();
    expect(screen.getByText('Test Client')).toBeInTheDocument();
    expect(screen.getByText('In Progress')).toBeInTheDocument();
    expect(screen.getByText('High')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('calls onView when view button is clicked', () => {
    const onView = jest.fn();
    renderWithProvider(<ProjectCard project={mockProject} onView={onView} />);
    
    fireEvent.click(screen.getByText('View'));
    expect(onView).toHaveBeenCalledWith(mockProject);
  });

  it('calls onEdit when edit button is clicked', () => {
    const onEdit = jest.fn();
    renderWithProvider(<ProjectCard project={mockProject} onEdit={onEdit} />);
    
    fireEvent.click(screen.getByText('Edit'));
    expect(onEdit).toHaveBeenCalledWith(mockProject);
  });
});
```

## 🚀 Deployment Configuration

### 1. Environment Configuration

```typescript
// src/config/environment.ts
interface AppConfig {
  API_URL: string;
  WS_URL: string;
  ENVIRONMENT: 'development' | 'staging' | 'production';
  SENTRY_DSN?: string;
  ANALYTICS_ID?: string;
}

const config: AppConfig = {
  API_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  WS_URL: process.env.REACT_APP_WS_URL || 'ws://localhost:8000',
  ENVIRONMENT: (process.env.NODE_ENV as AppConfig['ENVIRONMENT']) || 'development',
  SENTRY_DSN: process.env.REACT_APP_SENTRY_DSN,
  ANALYTICS_ID: process.env.REACT_APP_ANALYTICS_ID,
};

export default config;
```

### 2. Build Scripts

```json
// package.json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test",
    "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "type-check": "tsc --noEmit"
  }
}
```

This implementation guide provides a complete foundation for building the Ad Agency Project Manager frontend with modern React patterns, TypeScript, and comprehensive testing.

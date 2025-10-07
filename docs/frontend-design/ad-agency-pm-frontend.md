# 🎨 Ad Agency Project Manager - Frontend Design

## 📋 Design Overview

A modern, intuitive web interface for the Ad Agency Project Manager agent that provides both Solo Mode (traditional project management) and Squad Mode (multi-agent creative collaboration) capabilities.

## 🎯 Design Goals

- **User-Friendly**: Intuitive interface for project managers and creative teams
- **Dual-Mode Support**: Seamless switching between Solo and Squad modes
- **Real-Time Collaboration**: Live updates and notifications
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices
- **Accessibility**: WCAG 2.1 AA compliant
- **Performance**: Fast loading and smooth interactions

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Application                     │
├─────────────────────────────────────────────────────────────┤
│  React/Vue.js SPA                                          │
│  ├── Dashboard Components                                  │
│  ├── Project Management Views                              │
│  ├── Squad Mode Interface                                  │
│  ├── Real-time Chat/Notifications                          │
│  └── Analytics & Reporting                                 │
├─────────────────────────────────────────────────────────────┤
│  API Gateway / WebSocket Server                            │
├─────────────────────────────────────────────────────────────┤
│  Ad Agency PM Agent (Backend)                              │
│  ├── Solo Mode Tools                                       │
│  ├── Squad Mode Orchestration                              │
│  ├── Data Storage (JSON)                                   │
│  └── Sub-Agent Management                                  │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 UI/UX Design System

### Color Palette

```css
:root {
  /* Primary Colors */
  --primary-blue: #2563eb;
  --primary-blue-light: #3b82f6;
  --primary-blue-dark: #1d4ed8;
  
  /* Secondary Colors */
  --secondary-purple: #7c3aed;
  --secondary-purple-light: #8b5cf6;
  
  /* Accent Colors */
  --accent-green: #10b981;
  --accent-orange: #f59e0b;
  --accent-red: #ef4444;
  
  /* Neutral Colors */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  
  /* Status Colors */
  --status-success: #10b981;
  --status-warning: #f59e0b;
  --status-error: #ef4444;
  --status-info: #3b82f6;
}
```

### Typography

```css
/* Font Stack */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Heading Styles */
h1: 2.5rem (40px) / font-weight: 700 / line-height: 1.2
h2: 2rem (32px) / font-weight: 600 / line-height: 1.3
h3: 1.5rem (24px) / font-weight: 600 / line-height: 1.4
h4: 1.25rem (20px) / font-weight: 500 / line-height: 1.4

/* Body Text */
body: 1rem (16px) / font-weight: 400 / line-height: 1.6
small: 0.875rem (14px) / font-weight: 400 / line-height: 1.5
```

### Component Library

#### Buttons
```css
/* Primary Button */
.btn-primary {
  background: var(--primary-blue);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-1px);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: var(--primary-blue);
  border: 2px solid var(--primary-blue);
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
}

/* Squad Mode Toggle */
.btn-squad {
  background: linear-gradient(135deg, var(--secondary-purple), var(--primary-blue));
  color: white;
  padding: 1rem 2rem;
  border-radius: 1rem;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}
```

#### Cards
```css
.card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-200);
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-squad {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  border: 2px solid var(--secondary-purple);
}
```

## 📱 Screen Designs

### 1. Dashboard (Main Landing Page)

```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 Ad Agency PM                    [Solo Mode] [Squad Mode] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ 📊 Projects │  │ 👥 Team     │  │ 💰 Budget   │        │
│  │     12      │  │     8       │  │   $45,000   │        │
│  │ Active      │  │ Members     │  │ Remaining   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🚀 Quick Actions                                        │ │
│  │ [Create Project] [Add Client] [Schedule Meeting]       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 📅 Upcoming Deadlines                                   │ │
│  │ • Brand Identity - TechStart (Jan 15)                  │ │
│  │ • Social Campaign - EcoWear (Jan 18)                   │ │
│  │ • Website Launch - GreenTech (Jan 22)                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🎭 Squad Mode Status                                    │ │
│  │ [6 Specialists Ready] [Last Review: 2 hours ago]       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 2. Project Management View

```
┌─────────────────────────────────────────────────────────────┐
│ ← Back to Dashboard    📋 TechStart Brand Identity          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Project Overview                                        │ │
│  │ Status: In Progress | Budget: $25,000 | Due: Jan 15    │ │
│  │ Progress: ████████░░ 80%                               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────┐  ┌───────────────────────────────────┐ │
│  │ 📋 Tasks        │  │ 👥 Team Members                   │ │
│  │                 │  │                                   │ │
│  │ ✅ Logo Design  │  │ 🎨 Sarah (Art Director)          │ │
│  │ ✅ Brand Guide  │  │ ✍️ Mike (Copywriter)             │ │
│  │ 🔄 Website      │  │ 💻 Alex (Developer)              │ │
│  │ ⏳ Social Media │  │ 📱 Lisa (Social Media)           │ │
│  │                 │  │                                   │ │
│  │ [+ Add Task]    │  │ [+ Add Member]                   │ │
│  └─────────────────┘  └───────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 💬 Project Chat                                         │ │
│  │ Sarah: Logo concepts ready for review                  │ │
│  │ Mike: Brand voice guidelines completed                 │ │
│  │ [Type message...] [Send]                               │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3. Squad Mode Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🎭 Squad Mode - Creative Collaboration                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 📝 Creative Brief Input                                 │ │
│  │ ┌─────────────────────────────────────────────────────┐ │ │
│  │ │ We need a campaign for eco-friendly sneakers...     │ │ │
│  │ │ Target: Gen Z, Budget: $50k, Timeline: 6 weeks     │ │ │
│  │ └─────────────────────────────────────────────────────┘ │ │
│  │ [🎯 Run Squad Analysis]                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🎭 Specialist Analysis (Parallel)                      │ │
│  │                                                         │ │
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │ │
│  │ │👔 Account   │ │🎨 Creative  │ │🎯 Art       │       │ │
│  │ │Manager      │ │Director     │ │Director     │       │ │
│  │ │             │ │             │ │             │       │ │
│  │ │Brief: ✅    │ │Strategy: ✅ │ │Visuals: ✅  │       │ │
│  │ │Client: ✅   │ │Concept: ✅  │ │Mood: ✅     │       │ │
│  │ └─────────────┘ └─────────────┘ └─────────────┘       │ │
│  │                                                         │ │
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │ │
│  │ │✍️ Copywriter│ │📊 Strategy  │ │🎬 Production│       │ │
│  │ │             │ │Planner      │ │Manager      │       │ │
│  │ │Message: ✅  │ │Media: ✅    │ │Timeline: ✅ │       │ │
│  │ │Tone: ✅     │ │Audience: ✅ │ │Resources: ✅│       │ │
│  │ └─────────────┘ └─────────────┘ └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 🎯 Squad Synthesis (Creative Director)                  │ │
│  │ ┌─────────────────────────────────────────────────────┐ │ │
│  │ │ Complete campaign strategy with visual concepts,    │ │ │
│  │ │ messaging, media plan, and production timeline...   │ │ │
│  │ └─────────────────────────────────────────────────────┘ │ │
│  │ [📋 Create Project] [💾 Save Strategy] [📤 Export]    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4. Client Management

```
┌─────────────────────────────────────────────────────────────┐
│ 👥 Client Management                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ [🔍 Search clients...] [+ Add New Client]              │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 📋 Client List                                          │ │
│  │                                                         │ │
│  │ ┌─────────────────────────────────────────────────────┐ │ │
│  │ │ 🏢 TechStart Inc.                    [Edit] [View]  │ │ │
│  │ │ 📧 contact@techstart.com | 📞 (555) 123-4567       │ │ │
│  │ │ 🏭 Technology | 💰 $25,000 - $50,000               │ │ │
│  │ │ 📊 3 Active Projects | 📅 Last Contact: Jan 10     │ │ │
│  │ └─────────────────────────────────────────────────────┘ │ │
│  │                                                         │ │
│  │ ┌─────────────────────────────────────────────────────┐ │ │
│  │ │ 🌱 EcoWear Brand                    [Edit] [View]   │ │ │
│  │ │ 📧 hello@ecowear.com | 📞 (555) 987-6543           │ │ │
│  │ │ 👕 Fashion | 💰 $10,000 - $25,000                  │ │ │
│  │ │ 📊 2 Active Projects | 📅 Last Contact: Jan 12     │ │ │
│  │ └─────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Technical Architecture

### Frontend Stack

```json
{
  "framework": "React 18 with TypeScript",
  "styling": "Tailwind CSS + Styled Components",
  "state": "Redux Toolkit + RTK Query",
  "routing": "React Router v6",
  "ui": "Headless UI + Radix UI",
  "charts": "Recharts",
  "real-time": "Socket.io Client",
  "forms": "React Hook Form + Zod",
  "testing": "Jest + React Testing Library",
  "build": "Vite"
}
```

### Component Structure

```
src/
├── components/
│   ├── common/
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Modal/
│   │   ├── Input/
│   │   └── Loading/
│   ├── layout/
│   │   ├── Header/
│   │   ├── Sidebar/
│   │   ├── Navigation/
│   │   └── Footer/
│   ├── dashboard/
│   │   ├── StatsCards/
│   │   ├── QuickActions/
│   │   ├── UpcomingDeadlines/
│   │   └── RecentActivity/
│   ├── projects/
│   │   ├── ProjectList/
│   │   ├── ProjectCard/
│   │   ├── ProjectDetails/
│   │   ├── TaskList/
│   │   └── TeamMembers/
│   ├── squad/
│   │   ├── SquadModeToggle/
│   │   ├── BriefInput/
│   │   ├── SpecialistCards/
│   │   ├── AnalysisResults/
│   │   └── Synthesis/
│   └── clients/
│       ├── ClientList/
│       ├── ClientCard/
│       └── ClientForm/
├── pages/
│   ├── Dashboard/
│   ├── Projects/
│   ├── Clients/
│   ├── Squad/
│   └── Settings/
├── hooks/
│   ├── useWebSocket/
│   ├── useProjects/
│   ├── useSquad/
│   └── useClients/
├── store/
│   ├── slices/
│   │   ├── projectsSlice/
│   │   ├── clientsSlice/
│   │   ├── squadSlice/
│   │   └── uiSlice/
│   └── api/
│       ├── projectsApi/
│       ├── clientsApi/
│       └── squadApi/
└── utils/
    ├── api/
    ├── validation/
    └── helpers/
```

## 🔌 API Integration

### WebSocket Events

```typescript
// Real-time updates
interface WebSocketEvents {
  // Project updates
  'project:created': Project;
  'project:updated': Project;
  'project:deleted': { id: string };
  
  // Task updates
  'task:created': Task;
  'task:updated': Task;
  'task:assigned': { taskId: string; assignee: string };
  
  // Squad mode events
  'squad:analysis:started': { briefId: string };
  'squad:analysis:progress': { 
    briefId: string; 
    specialist: string; 
    progress: number 
  };
  'squad:analysis:completed': { 
    briefId: string; 
    results: SpecialistResult[] 
  };
  'squad:synthesis:completed': { 
    briefId: string; 
    synthesis: string 
  };
  
  // Notifications
  'notification:new': Notification;
  'notification:read': { id: string };
}
```

### REST API Endpoints

```typescript
// Projects
GET    /api/projects              // List all projects
POST   /api/projects              // Create new project
GET    /api/projects/:id          // Get project details
PUT    /api/projects/:id          // Update project
DELETE /api/projects/:id          // Delete project

// Tasks
GET    /api/projects/:id/tasks    // Get project tasks
POST   /api/projects/:id/tasks    // Create new task
PUT    /api/tasks/:id             // Update task
DELETE /api/tasks/:id             // Delete task

// Clients
GET    /api/clients               // List all clients
POST   /api/clients               // Create new client
GET    /api/clients/:id           // Get client details
PUT    /api/clients/:id           // Update client
DELETE /api/clients/:id           // Delete client

// Squad Mode
POST   /api/squad/analyze         // Start squad analysis
GET    /api/squad/analysis/:id    // Get analysis results
POST   /api/squad/synthesize      // Generate synthesis
```

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile First Approach */
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

### Mobile Layout

```
┌─────────────────────────┐
│ 🎯 Ad Agency PM    [☰]  │
├─────────────────────────┤
│                         │
│  ┌─────────────────────┐ │
│  │ 📊 Projects: 12     │ │
│  │ 👥 Team: 8          │ │
│  │ 💰 Budget: $45k     │ │
│  └─────────────────────┘ │
│                         │
│  ┌─────────────────────┐ │
│  │ 🚀 Quick Actions    │ │
│  │ [Create Project]    │ │
│  │ [Add Client]        │ │
│  │ [Schedule Meeting]  │ │
│  └─────────────────────┘ │
│                         │
│  ┌─────────────────────┐ │
│  │ 📅 Deadlines        │ │
│  │ • TechStart (Jan 15)│ │
│  │ • EcoWear (Jan 18)  │ │
│  │ • GreenTech (Jan 22)│ │
│  └─────────────────────┘ │
│                         │
│  ┌─────────────────────┐ │
│  │ 🎭 Squad Mode       │ │
│  │ [6 Specialists]     │ │
│  │ [Start Analysis]    │ │
│  └─────────────────────┘ │
└─────────────────────────┘
```

## 🎨 Interactive Features

### 1. Drag & Drop Task Management

```typescript
interface DragDropProps {
  tasks: Task[];
  onTaskMove: (taskId: string, newStatus: TaskStatus) => void;
  onTaskAssign: (taskId: string, assigneeId: string) => void;
}

// Kanban-style task board with drag & drop
const TaskBoard: React.FC<DragDropProps> = ({ tasks, onTaskMove, onTaskAssign }) => {
  return (
    <div className="grid grid-cols-4 gap-4">
      {['To Do', 'In Progress', 'Review', 'Done'].map(status => (
        <Droppable key={status} droppableId={status}>
          <div className="bg-gray-50 rounded-lg p-4 min-h-96">
            <h3 className="font-semibold mb-4">{status}</h3>
            {tasks.filter(task => task.status === status).map(task => (
              <Draggable key={task.id} draggableId={task.id} index={0}>
                <TaskCard task={task} />
              </Draggable>
            ))}
          </div>
        </Droppable>
      ))}
    </div>
  );
};
```

### 2. Real-time Squad Analysis

```typescript
const SquadAnalysis: React.FC = () => {
  const [analysisProgress, setAnalysisProgress] = useState<Record<string, number>>({});
  const [results, setResults] = useState<SpecialistResult[]>([]);
  
  useEffect(() => {
    const socket = io('/squad');
    
    socket.on('squad:analysis:progress', (data) => {
      setAnalysisProgress(prev => ({
        ...prev,
        [data.specialist]: data.progress
      }));
    });
    
    socket.on('squad:analysis:completed', (data) => {
      setResults(data.results);
    });
    
    return () => socket.disconnect();
  }, []);
  
  return (
    <div className="grid grid-cols-3 gap-4">
      {SPECIALISTS.map(specialist => (
        <SpecialistCard
          key={specialist.id}
          specialist={specialist}
          progress={analysisProgress[specialist.id] || 0}
          result={results.find(r => r.specialist === specialist.id)}
        />
      ))}
    </div>
  );
};
```

### 3. Interactive Project Timeline

```typescript
const ProjectTimeline: React.FC<{ project: Project }> = ({ project }) => {
  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <h3>Project Timeline</h3>
        <div className="timeline-controls">
          <button onClick={() => setView('gantt')}>Gantt View</button>
          <button onClick={() => setView('calendar')}>Calendar View</button>
        </div>
      </div>
      
      <div className="timeline-content">
        {project.phases.map((phase, index) => (
          <TimelinePhase
            key={phase.id}
            phase={phase}
            isActive={index === project.currentPhase}
            onPhaseClick={() => setActivePhase(phase.id)}
          />
        ))}
      </div>
    </div>
  );
};
```

## 🔒 Security & Performance

### Security Measures

```typescript
// API Security
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### Performance Optimizations

```typescript
// Code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Projects = lazy(() => import('./pages/Projects'));
const Squad = lazy(() => import('./pages/Squad'));

// Memoization for expensive components
const ProjectCard = memo(({ project }: { project: Project }) => {
  return (
    <div className="project-card">
      <h3>{project.name}</h3>
      <p>{project.description}</p>
      <ProgressBar value={project.progress} />
    </div>
  );
});

// Virtual scrolling for large lists
const ProjectList = () => {
  return (
    <FixedSizeList
      height={600}
      itemCount={projects.length}
      itemSize={120}
      itemData={projects}
    >
      {ProjectRow}
    </FixedSizeList>
  );
};
```

## 🧪 Testing Strategy

### Unit Tests

```typescript
// Component testing
describe('ProjectCard', () => {
  it('renders project information correctly', () => {
    const project = {
      id: '1',
      name: 'Test Project',
      description: 'Test Description',
      progress: 75
    };
    
    render(<ProjectCard project={project} />);
    
    expect(screen.getByText('Test Project')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '75');
  });
});
```

### Integration Tests

```typescript
// API integration testing
describe('Project API', () => {
  it('creates a new project', async () => {
    const projectData = {
      name: 'New Project',
      description: 'New Description',
      clientId: 'client-1'
    };
    
    const response = await apiClient.post('/projects', projectData);
    
    expect(response.status).toBe(201);
    expect(response.data.name).toBe('New Project');
  });
});
```

### E2E Tests

```typescript
// End-to-end testing with Playwright
test('user can create a new project', async ({ page }) => {
  await page.goto('/dashboard');
  
  await page.click('[data-testid="create-project-btn"]');
  await page.fill('[data-testid="project-name"]', 'E2E Test Project');
  await page.fill('[data-testid="project-description"]', 'E2E Test Description');
  await page.selectOption('[data-testid="client-select"]', 'client-1');
  
  await page.click('[data-testid="submit-project"]');
  
  await expect(page.locator('[data-testid="project-list"]')).toContainText('E2E Test Project');
});
```

## 🚀 Deployment & DevOps

### Build Configuration

```json
// package.json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "jest",
    "test:e2e": "playwright test",
    "lint": "eslint src --ext ts,tsx",
    "lint:fix": "eslint src --ext ts,tsx --fix"
  }
}
```

### Docker Configuration

```dockerfile
# Dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Configuration

```typescript
// Environment variables
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
  ENVIRONMENT: process.env.NODE_ENV as AppConfig['ENVIRONMENT'],
  SENTRY_DSN: process.env.REACT_APP_SENTRY_DSN,
  ANALYTICS_ID: process.env.REACT_APP_ANALYTICS_ID,
};
```

## 📊 Analytics & Monitoring

### User Analytics

```typescript
// Analytics tracking
const trackEvent = (eventName: string, properties?: Record<string, any>) => {
  if (config.ANALYTICS_ID) {
    gtag('event', eventName, {
      event_category: 'user_interaction',
      ...properties
    });
  }
};

// Usage tracking
const trackSquadAnalysis = (briefType: string, duration: number) => {
  trackEvent('squad_analysis_completed', {
    brief_type: briefType,
    duration_seconds: duration,
    specialists_count: 6
  });
};
```

### Performance Monitoring

```typescript
// Performance monitoring with Sentry
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: config.SENTRY_DSN,
  environment: config.ENVIRONMENT,
  integrations: [
    new Sentry.BrowserTracing(),
  ],
  tracesSampleRate: 0.1,
});

// Error boundary
const ErrorBoundary = Sentry.withErrorBoundary(App, {
  fallback: ({ error, resetError }) => (
    <div className="error-fallback">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={resetError}>Try again</button>
    </div>
  ),
});
```

This comprehensive frontend design provides a modern, intuitive interface for the Ad Agency Project Manager agent with full support for both Solo and Squad modes, real-time collaboration, and mobile responsiveness.

# 🏗️ Frontend Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Ad Agency PM Frontend                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        React SPA (TypeScript)                          │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │   Dashboard     │  │   Projects      │  │   Squad Mode    │        │   │
│  │  │   Components    │  │   Management    │  │   Interface     │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │   Client        │  │   Analytics     │  │   Settings      │        │   │
│  │  │   Management    │  │   & Reports     │  │   & Profile     │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  │                                                                         │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Shared Components                            │   │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │   │   │
│  │  │  │ Button  │ │  Card   │ │  Modal  │ │  Input  │ │ Loading │  │   │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        State Management                                │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │   Redux Store   │  │   RTK Query     │  │   WebSocket     │        │   │
│  │  │   (Global)      │  │   (API Cache)   │  │   (Real-time)   │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        Styling & UI                                    │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │   Tailwind CSS  │  │   Headless UI   │  │   Custom Theme  │        │   │
│  │  │   (Utility)     │  │   (Components)  │  │   (Design Sys)  │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/WebSocket
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        API Gateway / WebSocket Server                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        REST API Endpoints                              │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │   /api/projects │  │   /api/clients  │  │   /api/squad    │        │   │
│  │  │   CRUD Ops      │  │   CRUD Ops      │  │   Analysis      │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        WebSocket Events                                │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ project:*       │  │ client:*        │  │ squad:*         │        │   │
│  │  │ Real-time       │  │ Real-time       │  │ Real-time       │        │   │
│  │  │ Updates         │  │ Updates         │  │ Collaboration   │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Agent Communication
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    Ad Agency PM Agent (Backend)                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        Solo Mode Tools                                 │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ Client Mgmt     │  │ Project Mgmt    │  │ Task Mgmt       │        │   │
│  │  │ Tools           │  │ Tools           │  │ Tools           │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ Budget Tracking │  │ Team Mgmt       │  │ Reporting       │        │   │
│  │  │ Tools           │  │ Tools           │  │ Tools           │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        Squad Mode Orchestration                        │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ Account Manager │  │ Creative Dir    │  │ Art Director    │        │   │
│  │  │ Sub-Agent       │  │ Sub-Agent       │  │ Sub-Agent       │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ Copywriter      │  │ Strategy        │  │ Production      │        │   │
│  │  │ Sub-Agent       │  │ Planner         │  │ Manager         │        │   │
│  │  │                 │  │ Sub-Agent       │  │ Sub-Agent       │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        Data Storage (JSON)                             │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ clients.json    │  │ projects.json   │  │ tasks.json      │        │   │
│  │  │ Client Data     │  │ Project Data    │  │ Task Data       │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  │                                                                         │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │   │
│  │  │ teams.json      │  │ budgets.json    │  │ meetings.json   │        │   │
│  │  │ Team Data       │  │ Budget Data     │  │ Meeting Data    │        │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

```
App
├── Layout
│   ├── Header
│   │   ├── Logo
│   │   ├── Navigation
│   │   └── UserMenu
│   ├── Sidebar
│   │   ├── Navigation
│   │   └── SquadModeToggle
│   └── Main
│       ├── Dashboard
│       │   ├── StatsCards
│       │   ├── QuickActions
│       │   ├── UpcomingDeadlines
│       │   └── RecentActivity
│       ├── Projects
│       │   ├── ProjectList
│       │   ├── ProjectCard
│       │   ├── ProjectDetails
│       │   ├── TaskBoard
│       │   └── TeamMembers
│       ├── Clients
│       │   ├── ClientList
│       │   ├── ClientCard
│       │   └── ClientForm
│       └── Squad
│           ├── BriefInput
│           ├── SquadAnalysis
│           ├── SpecialistCards
│           └── Synthesis
└── Common Components
    ├── Button
    ├── Card
    ├── Modal
    ├── Input
    └── Loading
```

## Data Flow

```
User Interaction
       │
       ▼
┌─────────────┐
│   Component │
└─────────────┘
       │
       ▼
┌─────────────┐
│   Redux     │
│   Action    │
└─────────────┘
       │
       ▼
┌─────────────┐
│   RTK Query │
│   / WebSocket│
└─────────────┘
       │
       ▼
┌─────────────┐
│   API       │
│   Gateway   │
└─────────────┘
       │
       ▼
┌─────────────┐
│   Agent     │
│   Backend   │
└─────────────┘
       │
       ▼
┌─────────────┐
│   Data      │
│   Storage   │
└─────────────┘
       │
       ▼
┌─────────────┐
│   Response  │
│   / Event   │
└─────────────┘
       │
       ▼
┌─────────────┐
│   State     │
│   Update    │
└─────────────┘
       │
       ▼
┌─────────────┐
│   UI        │
│   Re-render │
└─────────────┘
```

## Technology Stack

```
Frontend Stack
├── React 18 + TypeScript
├── Redux Toolkit + RTK Query
├── React Router v6
├── Tailwind CSS + Headless UI
├── Socket.io Client
├── React Hook Form + Zod
├── Recharts (Charts)
├── @dnd-kit (Drag & Drop)
└── Vite (Build Tool)

Backend Integration
├── REST API (HTTP)
├── WebSocket (Real-time)
├── JSON Data Storage
└── Agent Tool System

Development Tools
├── Jest + RTL (Testing)
├── Playwright (E2E)
├── ESLint + Prettier
├── TypeScript
└── Docker (Deployment)
```

## Security & Performance

```
Security Layers
├── Input Validation (Zod)
├── XSS Protection
├── CSRF Protection
├── Authentication (JWT)
└── HTTPS/WSS

Performance Optimizations
├── Code Splitting (Lazy Loading)
├── Memoization (React.memo)
├── Virtual Scrolling
├── Image Optimization
├── Bundle Analysis
└── Caching (RTK Query)
```

This architecture provides a scalable, maintainable, and performant frontend solution for the Ad Agency Project Manager agent with full support for both Solo and Squad modes.

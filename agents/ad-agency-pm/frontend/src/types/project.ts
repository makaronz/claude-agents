export type ProjectStatus = 'Not Started' | 'In Progress' | 'Review' | 'Completed' | 'On Hold' | 'Cancelled';
export type Priority = 'Low' | 'Medium' | 'High' | 'Critical';

export interface TeamMember {
  id: string;
  name: string;
  role: string;
  avatar?: string;
  email?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  clientName: string;
  clientId: string;
  status: ProjectStatus;
  priority: Priority;
  progress: number; // 0-100
  budget: number;
  deadline: string;
  teamMembers: TeamMember[];
  createdAt: string;
  updatedAt: string;
}

export interface CreateProjectRequest {
  name: string;
  description: string;
  clientId: string;
  budget: number;
  deadline: string;
  priority: Priority;
  teamMembers?: string[]; // Array of team member IDs
}

export interface UpdateProjectRequest {
  id: string;
  name?: string;
  description?: string;
  clientId?: string;
  budget?: number;
  deadline?: string;
  priority?: Priority;
  status?: ProjectStatus;
  progress?: number;
  teamMembers?: string[];
}

export type TaskStatus = 'To Do' | 'In Progress' | 'Review' | 'Done';

export interface Task {
  id: string;
  projectId: string;
  title: string;
  description?: string;
  status: TaskStatus;
  assignee?: TeamMember;
  dueDate?: string;
  priority: Priority;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTaskRequest {
  projectId: string;
  title: string;
  description?: string;
  assigneeId?: string;
  dueDate?: string;
  priority: Priority;
}

export interface UpdateTaskRequest {
  id: string;
  title?: string;
  description?: string;
  status?: TaskStatus;
  assigneeId?: string;
  dueDate?: string;
  priority?: Priority;
}

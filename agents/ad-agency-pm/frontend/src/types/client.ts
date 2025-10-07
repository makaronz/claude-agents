export interface Client {
  id: string;
  name: string;
  email: string;
  phone?: string;
  company?: string;
  industry?: string;
  budgetRange?: string;
  notes?: string;
  activeProjects: number;
  lastContact?: string;
  createdAt: string;
  updatedAt: string;
}

export interface CreateClientRequest {
  name: string;
  email: string;
  phone?: string;
  company?: string;
  industry?: string;
  budgetRange?: string;
  notes?: string;
}

export interface UpdateClientRequest {
  id: string;
  name?: string;
  email?: string;
  phone?: string;
  company?: string;
  industry?: string;
  budgetRange?: string;
  notes?: string;
}

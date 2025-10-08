import React, { useState, useEffect } from 'react';
import { Button } from '@/components/common/Button';
import { ProjectList } from '@/components/projects/ProjectList';
import { Modal } from '@/components/common/Modal';
import { useProjects, useFilteredProjects, useProjectContext } from '@/context';
import type { Project } from '@/types/project';

const Projects: React.FC = () => {
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  
  const { state, setLoading, setError } = useProjectContext();
  const filteredProjects = useFilteredProjects();

  // Load projects on mount (mock data for now)
  useEffect(() => {
    const loadProjects = async () => {
      setLoading(true);
      try {
        // Mock data - replace with actual API call
        const mockProjects: Project[] = [
          {
            id: '1',
            name: 'Nike Campaign',
            description: 'Summer 2024 sneaker launch campaign',
            clientId: 'client-1',
            status: 'In Progress',
            priority: 'High',
            progress: 75,
            budget: 250000,
            deadline: '2024-06-15',
            teamMembers: ['creative-director', 'copywriter', 'art-director'],
            createdAt: '2024-01-15',
            updatedAt: '2024-02-10',
          },
          {
            id: '2',
            name: 'Apple Watch Ad',
            description: 'New Apple Watch Series 10 advertisement',
            clientId: 'client-2',
            status: 'Planning',
            priority: 'Medium',
            progress: 25,
            budget: 180000,
            deadline: '2024-07-01',
            teamMembers: ['creative-director', 'production-manager'],
            createdAt: '2024-02-01',
            updatedAt: '2024-02-05',
          },
        ];
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // In real app, this would come from API
        // For now, we'll add them to context
        mockProjects.forEach(project => {
          // This would be handled by the context action
        });
        
        setLoading(false);
      } catch (error) {
        setError('Failed to load projects');
        setLoading(false);
      }
    };

    loadProjects();
  }, [setLoading, setError]);

  const handleView = (project: Project) => {
    setSelectedProject(project);
    // TODO: Navigate to project details page or open modal
  };

  const handleEdit = (project: Project) => {
    setSelectedProject(project);
    // TODO: Open edit modal
  };

  const handleDelete = (project: Project) => {
    if (confirm(`Are you sure you want to delete "${project.name}"?`)) {
      // TODO: Implement delete with mutation
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
          <p className="text-sm text-gray-600 mt-1">
            {filteredProjects.length} project{filteredProjects.length !== 1 ? 's' : ''}
          </p>
        </div>
        <Button onClick={() => setCreateModalOpen(true)}>+ New Project</Button>
      </div>

      <ProjectList
        projects={filteredProjects}
        loading={state.loading}
        error={state.error}
        onView={handleView}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      {/* Create Project Modal */}
      <Modal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        title="Create New Project"
        size="lg"
      >
        <p className="text-gray-600">
          Project creation form will be implemented here.
        </p>
      </Modal>
    </div>
  );
};

export default Projects;

import React, { useState } from 'react';
import { Button } from '@/components/common/Button';
import { ProjectList } from '@/components/projects/ProjectList';
import { Modal } from '@/components/common/Modal';
import { useGetProjectsQuery } from '@/store/api/projectsApi';
import { useAppSelector } from '@/store/hooks';
import type { Project } from '@/types/project';

const Projects: React.FC = () => {
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  
  const { data: projects = [], isLoading, error } = useGetProjectsQuery();
  const filters = useAppSelector((state) => state.projects.filters);

  // Filter projects based on active filters
  const filteredProjects = projects.filter((project) => {
    if (filters.search && !project.name.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    if (filters.status.length > 0 && !filters.status.includes(project.status)) {
      return false;
    }
    if (filters.priority.length > 0 && !filters.priority.includes(project.priority)) {
      return false;
    }
    if (filters.client.length > 0 && !filters.client.includes(project.clientId)) {
      return false;
    }
    return true;
  });

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
        loading={isLoading}
        error={error ? 'Failed to load projects' : null}
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

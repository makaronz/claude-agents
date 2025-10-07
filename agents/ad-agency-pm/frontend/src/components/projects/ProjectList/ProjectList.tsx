import React from 'react';
import { ProjectCard } from '../ProjectCard';
import { Loading } from '@/components/common/Loading';
import type { Project } from '@/types/project';
import { cn } from '@/utils/helpers';

export interface ProjectListProps {
  projects: Project[];
  loading?: boolean;
  error?: string | null;
  onEdit?: (project: Project) => void;
  onView?: (project: Project) => void;
  onDelete?: (project: Project) => void;
  viewMode?: 'grid' | 'list';
  className?: string;
}

const ProjectList: React.FC<ProjectListProps> = ({
  projects,
  loading = false,
  error = null,
  onEdit,
  onView,
  onDelete,
  viewMode = 'grid',
  className,
}) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <Loading text="Loading projects..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <p className="text-error text-lg mb-2">Failed to load projects</p>
          <p className="text-gray-600 text-sm">{error}</p>
        </div>
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <p className="text-gray-600 text-lg mb-2">No projects found</p>
          <p className="text-gray-500 text-sm">Create your first project to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        viewMode === 'grid'
          ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6'
          : 'space-y-4',
        className
      )}
    >
      {projects.map((project) => (
        <ProjectCard
          key={project.id}
          project={project}
          onEdit={onEdit}
          onView={onView}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

ProjectList.displayName = 'ProjectList';

export default ProjectList;


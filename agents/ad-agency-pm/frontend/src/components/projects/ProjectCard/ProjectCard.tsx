import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import type { Project } from '@/types/project';
import { cn, formatCurrency, formatDate, getStatusColor, getPriorityColor, getInitials } from '@/utils/helpers';

export interface ProjectCardProps {
  project: Project;
  onEdit?: (project: Project) => void;
  onView?: (project: Project) => void;
  onDelete?: (project: Project) => void;
  className?: string;
}

const ProjectCard: React.FC<ProjectCardProps> = ({
  project,
  onEdit,
  onView,
  onDelete,
  className,
}) => {
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
          <div className="flex flex-col items-end space-y-2">
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
              <span className="font-medium">{project.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={cn(
                  'h-2 rounded-full transition-all duration-300',
                  project.progress < 30 && 'bg-red-500',
                  project.progress >= 30 && project.progress < 70 && 'bg-yellow-500',
                  project.progress >= 70 && 'bg-green-500'
                )}
                style={{ width: `${project.progress}%` }}
              />
            </div>
          </div>

          {/* Project Details */}
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-500">Budget:</span>
              <span className="ml-1 font-medium">{formatCurrency(project.budget)}</span>
            </div>
            <div>
              <span className="text-gray-500">Due:</span>
              <span className="ml-1 font-medium">
                {formatDate(project.deadline)}
              </span>
            </div>
          </div>

          {/* Team Members */}
          {project.teamMembers && project.teamMembers.length > 0 && (
            <div>
              <span className="text-sm text-gray-500">Team:</span>
              <div className="flex -space-x-2 mt-1">
                {project.teamMembers.slice(0, 4).map((member, index) => (
                  <div
                    key={member.id}
                    className="w-8 h-8 rounded-full bg-primary-600 border-2 border-white flex items-center justify-center text-xs font-medium text-white"
                    title={member.name}
                  >
                    {getInitials(member.name)}
                  </div>
                ))}
                {project.teamMembers.length > 4 && (
                  <div className="w-8 h-8 rounded-full bg-gray-200 border-2 border-white flex items-center justify-center text-xs font-medium text-gray-600">
                    +{project.teamMembers.length - 4}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-2 pt-2">
            {onView && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => onView(project)}
                className="flex-1"
              >
                View
              </Button>
            )}
            {onEdit && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onEdit(project)}
                className="flex-1"
              >
                Edit
              </Button>
            )}
            {onDelete && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onDelete(project)}
                className="text-error hover:text-error hover:bg-red-50"
              >
                Delete
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

ProjectCard.displayName = 'ProjectCard';

export default ProjectCard;


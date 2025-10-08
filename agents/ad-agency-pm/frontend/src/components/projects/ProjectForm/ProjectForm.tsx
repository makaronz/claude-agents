import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { Textarea } from '@/components/common/Textarea';
import { Select } from '@/components/common/Select';
import { useProjectContext } from '@/context';
import { useClients } from '@/context';
import type { CreateProjectRequest, Priority } from '@/types/project';

// Mock team members for now
const MOCK_TEAM_MEMBERS = [
  { id: 'creative-director', name: 'John Doe', role: 'Creative Director' },
  { id: 'copywriter', name: 'Jane Smith', role: 'Copywriter' },
  { id: 'art-director', name: 'Peter Jones', role: 'Art Director' },
  { id: 'production-manager', name: 'Alice Brown', role: 'Production Manager' },
  { id: 'account-manager', name: 'Mike Wilson', role: 'Account Manager' },
  { id: 'strategy-planner', name: 'Sarah Davis', role: 'Strategy Planner' },
];

const PRIORITY_OPTIONS = [
  { value: 'Low', label: 'Low Priority' },
  { value: 'Medium', label: 'Medium Priority' },
  { value: 'High', label: 'High Priority' },
  { value: 'Critical', label: 'Critical Priority' },
] as const;

// Validation schema
const projectSchema = z.object({
  name: z.string().min(1, 'Project name is required').max(100, 'Name too long'),
  description: z.string().min(10, 'Description must be at least 10 characters').max(500, 'Description too long'),
  clientId: z.string().min(1, 'Please select a client'),
  budget: z.number().min(0, 'Budget must be positive').max(10000000, 'Budget too high'),
  deadline: z.string().min(1, 'Deadline is required'),
  priority: z.enum(['Low', 'Medium', 'High', 'Critical'] as const),
  teamMembers: z.array(z.string()).min(1, 'Select at least one team member'),
});

type ProjectFormData = z.infer<typeof projectSchema>;

interface ProjectFormProps {
  onSuccess?: () => void;
  onCancel?: () => void;
  initialData?: Partial<CreateProjectRequest>;
}

export const ProjectForm: React.FC<ProjectFormProps> = ({
  onSuccess,
  onCancel,
  initialData,
}) => {
  const { addProject } = useProjectContext();
  const clients = useClients();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch,
    setValue,
  } = useForm<ProjectFormData>({
    resolver: zodResolver(projectSchema),
    defaultValues: {
      name: initialData?.name || '',
      description: initialData?.description || '',
      clientId: initialData?.clientId || '',
      budget: initialData?.budget || 0,
      deadline: initialData?.deadline || '',
      priority: initialData?.priority || 'Medium',
      teamMembers: initialData?.teamMembers || [],
    },
  });

  const selectedTeamMembers = watch('teamMembers');

  const onSubmit = async (data: ProjectFormData) => {
    try {
      // Generate new project ID
      const newProject = {
        id: `project-${Date.now()}`,
        name: data.name,
        description: data.description,
        clientId: data.clientId,
        clientName: clients.find(c => c.id === data.clientId)?.name || 'Unknown Client',
        status: 'Not Started' as const,
        priority: data.priority,
        progress: 0,
        budget: data.budget,
        deadline: data.deadline,
        teamMembers: data.teamMembers.map(memberId => {
          const member = MOCK_TEAM_MEMBERS.find(m => m.id === memberId);
          return member || { id: memberId, name: 'Unknown', role: 'Team Member' };
        }),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      // Add project to context
      addProject(newProject);

      // Call success callback
      onSuccess?.();

    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  const handleTeamMemberToggle = (memberId: string) => {
    const currentMembers = selectedTeamMembers;
    const newMembers = currentMembers.includes(memberId)
      ? currentMembers.filter(id => id !== memberId)
      : [...currentMembers, memberId];
    
    setValue('teamMembers', newMembers);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Project Name */}
      <div>
        <Input
          label="Project Name"
          {...register('name')}
          error={errors.name?.message}
          placeholder="Enter project name"
          required
        />
      </div>

      {/* Description */}
      <div>
        <Textarea
          label="Description"
          {...register('description')}
          error={errors.description?.message}
          placeholder="Describe the project goals, requirements, and deliverables..."
          rows={4}
          required
        />
      </div>

      {/* Client Selection */}
      <div>
        <Select
          label="Client"
          {...register('clientId')}
          error={errors.clientId?.message}
          required
        >
          <option value="">Select a client</option>
          {clients.map((client) => (
            <option key={client.id} value={client.id}>
              {client.name} {client.company && `(${client.company})`}
            </option>
          ))}
          {clients.length === 0 && (
            <option value="" disabled>
              No clients available - Add clients first
            </option>
          )}
        </Select>
      </div>

      {/* Budget and Deadline Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <Input
            label="Budget ($)"
            type="number"
            {...register('budget', { valueAsNumber: true })}
            error={errors.budget?.message}
            placeholder="0"
            min="0"
            step="100"
            required
          />
        </div>
        <div>
          <Input
            label="Deadline"
            type="date"
            {...register('deadline')}
            error={errors.deadline?.message}
            min={new Date().toISOString().split('T')[0]}
            required
          />
        </div>
      </div>

      {/* Priority */}
      <div>
        <Select
          label="Priority"
          {...register('priority')}
          error={errors.priority?.message}
          required
        >
          {PRIORITY_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </div>

      {/* Team Members */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Team Members <span className="text-red-500">*</span>
        </label>
        {errors.teamMembers && (
          <p className="text-red-500 text-sm mt-1">{errors.teamMembers.message}</p>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {MOCK_TEAM_MEMBERS.map((member) => (
            <label
              key={member.id}
              className="flex items-center space-x-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <input
                type="checkbox"
                checked={selectedTeamMembers.includes(member.id)}
                onChange={() => handleTeamMemberToggle(member.id)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">{member.name}</p>
                <p className="text-xs text-gray-500">{member.role}</p>
              </div>
            </label>
          ))}
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Selected: {selectedTeamMembers.length} member{selectedTeamMembers.length !== 1 ? 's' : ''}
        </p>
      </div>

      {/* Form Actions */}
      <div className="flex justify-end space-x-3 pt-6 border-t">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={isSubmitting}
          loading={isSubmitting}
        >
          {isSubmitting ? 'Creating...' : 'Create Project'}
        </Button>
      </div>
    </form>
  );
};

export default ProjectForm;

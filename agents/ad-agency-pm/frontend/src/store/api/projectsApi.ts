import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import type {
  Project,
  CreateProjectRequest,
  UpdateProjectRequest,
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
} from '@/types/project';
import config from '@/config/environment';

export const projectsApi = createApi({
  reducerPath: 'projectsApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${config.API_URL}/api/projects`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Project', 'Task'],
  endpoints: (builder) => ({
    // Projects
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

    // Tasks
    getProjectTasks: builder.query<Task[], string>({
      query: (projectId) => `/${projectId}/tasks`,
      providesTags: (result, error, projectId) => [
        { type: 'Task', id: `PROJECT_${projectId}` },
      ],
    }),
    createTask: builder.mutation<Task, CreateTaskRequest>({
      query: ({ projectId, ...task }) => ({
        url: `/${projectId}/tasks`,
        method: 'POST',
        body: task,
      }),
      invalidatesTags: (result, error, { projectId }) => [
        { type: 'Task', id: `PROJECT_${projectId}` },
      ],
    }),
    updateTask: builder.mutation<Task, UpdateTaskRequest>({
      query: ({ id, ...task }) => ({
        url: `/tasks/${id}`,
        method: 'PUT',
        body: task,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Task', id }],
    }),
    deleteTask: builder.mutation<void, string>({
      query: (id) => ({
        url: `/tasks/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Task'],
    }),
  }),
});

export const {
  useGetProjectsQuery,
  useGetProjectQuery,
  useCreateProjectMutation,
  useUpdateProjectMutation,
  useDeleteProjectMutation,
  useGetProjectTasksQuery,
  useCreateTaskMutation,
  useUpdateTaskMutation,
  useDeleteTaskMutation,
} = projectsApi;


import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import {
  SquadAnalysisRequest,
  SquadAnalysisResponse,
  SquadSynthesis,
} from '@/types/squad';
import config from '@/config/environment';

export const squadApi = createApi({
  reducerPath: 'squadApi',
  baseQuery: fetchBaseQuery({
    baseUrl: `${config.API_URL}/api/squad`,
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Analysis'],
  endpoints: (builder) => ({
    startAnalysis: builder.mutation<
      { briefId: string; status: string },
      SquadAnalysisRequest
    >({
      query: (request) => ({
        url: '/analyze',
        method: 'POST',
        body: request,
      }),
      invalidatesTags: ['Analysis'],
    }),
    getAnalysis: builder.query<SquadAnalysisResponse, string>({
      query: (briefId) => `/analysis/${briefId}`,
      providesTags: (result, error, briefId) => [{ type: 'Analysis', id: briefId }],
    }),
    getSynthesis: builder.query<SquadSynthesis, string>({
      query: (briefId) => `/synthesis/${briefId}`,
      providesTags: (result, error, briefId) => [{ type: 'Analysis', id: `${briefId}_synthesis` }],
    }),
    getAnalysisHistory: builder.query<SquadAnalysisResponse[], void>({
      query: () => '/history',
      providesTags: ['Analysis'],
    }),
  }),
});

export const {
  useStartAnalysisMutation,
  useGetAnalysisQuery,
  useGetSynthesisQuery,
  useGetAnalysisHistoryQuery,
} = squadApi;


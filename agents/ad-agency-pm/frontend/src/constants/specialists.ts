import { Specialist, SpecialistType } from '@/types/squad';

export const SPECIALISTS: Specialist[] = [
  {
    id: 'account-manager' as SpecialistType,
    name: 'Account Manager',
    role: 'Brief Analysis & Client Relations',
    icon: '👔',
    color: 'bg-blue-500',
    description: 'Analyzes client brief, validates requirements, and identifies strategic objectives',
  },
  {
    id: 'creative-director' as SpecialistType,
    name: 'Creative Director',
    role: 'Overall Strategy & Vision',
    icon: '🎨',
    color: 'bg-purple-500',
    description: 'Develops overarching creative strategy and synthesizes team insights',
  },
  {
    id: 'art-director' as SpecialistType,
    name: 'Art Director',
    role: 'Visual Concepts & Design',
    icon: '🎯',
    color: 'bg-green-500',
    description: 'Creates visual concepts, mood boards, and design direction',
  },
  {
    id: 'copywriter' as SpecialistType,
    name: 'Copywriter',
    role: 'Messaging & Copy',
    icon: '✍️',
    color: 'bg-orange-500',
    description: 'Crafts compelling messaging, headlines, and campaign copy',
  },
  {
    id: 'strategy-planner' as SpecialistType,
    name: 'Strategy Planner',
    role: 'Media Strategy & Audience',
    icon: '📊',
    color: 'bg-red-500',
    description: 'Develops media strategy, identifies target audiences, and plans channels',
  },
  {
    id: 'production-manager' as SpecialistType,
    name: 'Production Manager',
    role: 'Timeline & Resources',
    icon: '🎬',
    color: 'bg-indigo-500',
    description: 'Plans production timeline, resource allocation, and deliverables',
  },
];

export const getSpecialistById = (id: SpecialistType): Specialist | undefined => {
  return SPECIALISTS.find((s) => s.id === id);
};

export const getSpecialistColor = (id: SpecialistType): string => {
  const specialist = getSpecialistById(id);
  return specialist?.color || 'bg-gray-500';
};


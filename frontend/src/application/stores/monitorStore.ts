// Monitor Store - Application state management using Zustand

import { create } from 'zustand'
import { Monitor } from '@/domain/types'
import { apiClient } from '@/infrastructure/api/client'

interface MonitorStore {
  // State
  monitors: Monitor[]
  currentMonitor: Monitor | null
  loading: boolean
  error: string | null
  total: number

  // Actions
  fetchMonitors: (skip?: number, limit?: number) => Promise<void>
  fetchMonitor: (id: string) => Promise<void>
  createMonitor: (data: any) => Promise<Monitor>
  clearError: () => void
  reset: () => void
}

export const useMonitorStore = create<MonitorStore>((set) => ({
  monitors: [],
  currentMonitor: null,
  loading: false,
  error: null,
  total: 0,

  fetchMonitors: async (skip = 0, limit = 20) => {
    set({ loading: true, error: null })
    try {
      const data = await apiClient.listMonitors(skip, limit)
      set({
        monitors: data.items,
        total: data.total,
        loading: false,
      })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch monitors',
        loading: false,
      })
    }
  },

  fetchMonitor: async (id: string) => {
    set({ loading: true, error: null })
    try {
      const monitor = await apiClient.getMonitor(id)
      set({
        currentMonitor: monitor,
        loading: false,
      })
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to fetch monitor',
        loading: false,
      })
    }
  },

  createMonitor: async (data: any) => {
    set({ loading: true, error: null })
    try {
      const monitor = await apiClient.createMonitor(data)
      set((state) => ({
        monitors: [monitor, ...state.monitors],
        loading: false,
      }))
      return monitor
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Failed to create monitor',
        loading: false,
      })
      throw error
    }
  },

  clearError: () => set({ error: null }),
  reset: () =>
    set({
      monitors: [],
      currentMonitor: null,
      loading: false,
      error: null,
      total: 0,
    }),
}))

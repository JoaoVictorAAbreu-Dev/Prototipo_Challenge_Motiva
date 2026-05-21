// API Client - Infrastructure layer

import axios, { AxiosInstance, AxiosError } from 'axios'
import {
  Monitor,
  MonitorList,
  CreateMonitorRequest,
  ApiError,
  GenerateClustersRequest,
  InterventionCluster,
} from '@/domain/types'

class ApiClient {
  private client: AxiosInstance

  constructor(baseURL: string = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Response interceptor
    this.client.interceptors.response.use(
      response => response,
      error => this.handleError(error),
    )
  }

  private handleError(error: AxiosError<ApiError>) {
    if (error.response?.status === 404) {
      throw new Error(error.response?.data?.detail || 'Resource not found')
    }
    if (error.response?.status === 400) {
      throw new Error(error.response?.data?.detail || 'Bad request')
    }
    if (error.response?.status === 500) {
      throw new Error('Internal server error')
    }
    throw error
  }

  // Monitor endpoints
  async createMonitor(data: CreateMonitorRequest): Promise<Monitor> {
    const response = await this.client.post<Monitor>('/monitors', data)
    return response.data
  }

  async getMonitor(id: string): Promise<Monitor> {
    const response = await this.client.get<Monitor>(`/monitors/${id}`)
    return response.data
  }

  async listMonitors(skip: number = 0, limit: number = 20): Promise<MonitorList> {
    const response = await this.client.get<MonitorList>('/monitors', {
      params: { skip, limit },
    })
    return response.data
  }

  async generateClusters(
    data: GenerateClustersRequest,
  ): Promise<InterventionCluster[]> {
    const response = await this.client.post<InterventionCluster[]>(
      '/generate-clusters',
      data,
    )
    return response.data
  }
}

export const apiClient = new ApiClient()

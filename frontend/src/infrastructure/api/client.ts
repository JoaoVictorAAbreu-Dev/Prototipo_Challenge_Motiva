// API Client - Infrastructure layer

import axios, { AxiosInstance, AxiosError } from 'axios'
import {
  ApiError,
  GenerateClustersRequest,
  InterventionCluster,
  MicroSegmentList,
  OperationalMicroSegment,
  SimulationProjectionRequest,
  SimulationProjectionResponse,
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

  async generateClusters(
    data: GenerateClustersRequest,
  ): Promise<InterventionCluster[]> {
    const response = await this.client.post<InterventionCluster[]>(
      '/generate-clusters',
      data,
    )
    return response.data
  }

  async listMicrosegments(
    skip: number = 0,
    limit: number = 250,
  ): Promise<MicroSegmentList> {
    const response = await this.client.get<MicroSegmentList>('/microsegments', {
      params: { skip, limit },
    })
    return response.data
  }

  async getMicrosegment(id: string): Promise<OperationalMicroSegment> {
    const response = await this.client.get<OperationalMicroSegment>(
      `/microsegments/${id}`,
    )
    return response.data
  }

  async projectSimulation(
    data: SimulationProjectionRequest,
  ): Promise<SimulationProjectionResponse> {
    const response = await this.client.post<SimulationProjectionResponse>(
      '/simulation/project',
      data,
    )
    return response.data
  }

  async exportComplianceReport(segmentId: string): Promise<Blob> {
    const response = await this.client.get(`/export-compliance-report/${segmentId}`, {
      responseType: 'blob',
    })
    return response.data as Blob
  }
}

export const apiClient = new ApiClient()

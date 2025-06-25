// API Client for ASMIS Frontend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

export class APIClient {
  private baseURL: string
  private wsURL: string

  constructor(baseURL?: string, wsURL?: string) {
    this.baseURL = baseURL || API_BASE_URL
    this.wsURL = wsURL || WS_BASE_URL
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new APIError(
          errorData.message || `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData.code
        )
      }

      return await response.json()
    } catch (error) {
      if (error instanceof APIError) {
        throw error
      }
      
      throw new APIError(
        `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        0
      )
    }
  }

  // GET request
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  // POST request
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // PUT request
  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  // DELETE request
  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }

  // WebSocket connection
  createWebSocket(path: string): WebSocket {
    const url = `${this.wsURL}${path}`
    return new WebSocket(url)
  }

  // File upload
  async uploadFile<T>(
    endpoint: string, 
    file: File, 
    additionalData?: Record<string, string>
  ): Promise<T> {
    const formData = new FormData()
    formData.append('file', file)
    
    if (additionalData) {
      Object.entries(additionalData).forEach(([key, value]) => {
        formData.append(key, value)
      })
    }

    return this.request<T>(endpoint, {
      method: 'POST',
      body: formData,
      headers: {}, // Don't set Content-Type for FormData
    })
  }
}

// Default client instance
export const apiClient = new APIClient()

// Request interceptors for authentication, logging, etc.
export const withAuth = (token: string) => ({
  Authorization: `Bearer ${token}`,
})

// Response transformers
export const transformDateStrings = (obj: any): any => {
  if (!obj || typeof obj !== 'object') return obj
  
  if (Array.isArray(obj)) {
    return obj.map(transformDateStrings)
  }
  
  const transformed: any = {}
  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'string' && /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/.test(value)) {
      transformed[key] = new Date(value)
    } else if (typeof value === 'object') {
      transformed[key] = transformDateStrings(value)
    } else {
      transformed[key] = value
    }
  }
  
  return transformed
}
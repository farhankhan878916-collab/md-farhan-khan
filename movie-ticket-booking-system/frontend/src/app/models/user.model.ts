export interface User {
  id: number;
  username: string;
  email: string;
  fullName: string;
  phone?: string;
  role: 'ROLE_ADMIN' | 'ROLE_CUSTOMER' | string;
  active: boolean;
}

export interface AuthResponse {
  token: string;
  type: string;
  id: number;
  username: string;
  email: string;
  fullName: string;
  role: string;
}

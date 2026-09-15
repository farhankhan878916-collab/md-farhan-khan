export interface Theatre {
  id: number;
  name: string;
  address: string;
  city: string;
  state?: string;
  zipCode?: string;
  totalScreens: number;
  active: boolean;
}

export interface Screen {
  id: number;
  name: string;
  totalRows: number;
  totalColumns: number;
  theatreId: number;
  theatreName: string;
}

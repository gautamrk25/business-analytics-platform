import { createContext } from 'react';
import { Practice } from '../interfaces/types';

export interface AppState {
    practices: Practice[];
}

export const AppContext = createContext<AppState>({ practices: [] });
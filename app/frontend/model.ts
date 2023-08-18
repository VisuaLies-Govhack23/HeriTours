import { create } from 'zustand';

export enum Page {
    home = 'home',
    map = 'map',
    details = 'details'
}

interface AppState {
    page: Page;
}

export const useAppStore = create<AppState>(() => ({
    page: Page.map
}));

export const search = (query: string) => {
    console.log('search for', query);
    useAppStore.setState(state => ({ ...state, page: Page.map }));
};

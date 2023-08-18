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
    page: Page.home
}));

export const search = (query: string) => {
    console.log('search for', query);
    useAppStore.setState(state => ({ ...state, page: Page.map }));
};

export const initGeolocation = async () => {
    if ('geolocation' in navigator) {
        navigator.geolocation.watchPosition(position => {
            console.log('position is', position);
        });
    }
};

import { LatLngTuple } from 'leaflet';
import { create } from 'zustand';

export enum Page {
    home = 'home',
    map = 'map',
    details = 'details'
}

interface AppState {
    page: Page;
    tour: string;
    positionLatLng: LatLngTuple | null;
}

export const useAppStore = create<AppState>(() => ({
    page: Page.home,
    tour: 'Tour',
    positionLatLng: null
}));

export const home = () => {
    useAppStore.setState(state => ({ ...state, page: Page.home }));
};

export const search = (query: string) => {
    console.log('search for', query);
    useAppStore.setState(state => ({ ...state, page: Page.map }));
};

export const initGeolocation = () => {
    if ('geolocation' in navigator) {
        navigator.geolocation.watchPosition(position => {
            console.log('position is', position);
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            useAppStore.setState(state => ({ ...state, positionLatLng: [lat, lng] }));
        });
    }
};

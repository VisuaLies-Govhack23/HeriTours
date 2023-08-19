import { LatLngTuple } from 'leaflet';
import { create } from 'zustand';
import { SiteInfoData } from './types';

export enum Page {
    home = 'home',
    map = 'map',
    details = 'details'
}

let idGenerator = 1;

interface AppState {
    page: Page;
    tour: string;
    positionLatLng: LatLngTuple | null;
    loaders: number[];
}

export const useAppStore = create<AppState>(() => ({
    page: Page.home,
    tour: 'Tour',
    positionLatLng: null,
    loaders: []
}));

export const home = () => {
    useAppStore.setState(state => ({ ...state, page: Page.home }));
};

export const search = (query: string) => {
    console.log('search for', query);
    const words = query.split(' ');
    const capitalized = words.map(word =>
        word.match(/^[a-z]/) ? `${word.charAt(0).toUpperCase()}${word.substring(1)}` : word
    );
    const title = capitalized.join(' ');
    useAppStore.setState(state => ({ ...state, page: Page.map, tour: title }));
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

export const loadSite = async (siteId: string): Promise<SiteInfoData> => {
    const id = idGenerator++;
    try {
        useAppStore.setState(state => ({ ...state, loaders: [...state.loaders, id] }));

        const result = await fetch(`/site/${siteId}`, {
            credentials: 'include'
        });
        const json = (await result.json()) as SiteInfoData;
        return json;
    } finally {
        // Remove from queue of pending requests
        useAppStore.setState(state => ({ ...state, loaders: state.loaders.filter(item => item != id) }));
    }
};

export const sendVote = async (siteId: string, vote: number): Promise<void> => {
    // No need to show a loader during this operation
    await fetch(`/vote/${siteId}/${vote}`, {
        credentials: 'include',
        method: 'POST'
    });
};

export const sendAnswer = async (siteId: string, questionId: string, answerId: string): Promise<void> => {
    // No need to show a loader during this operation
    await fetch(`/answer/${siteId}/${questionId}/${answerId}`, {
        credentials: 'include',
        method: 'POST'
    });
};

export const sendStory = async (siteId: string, story: string): Promise<void> => {
    // No need to show a loader during this operation
    await fetch(`/story/${siteId}`, {
        credentials: 'include',
        method: 'POST',
        body: story
    });
};

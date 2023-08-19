import { LatLngTuple } from 'leaflet';
import { create } from 'zustand';
import { ItemData, SiteInfoData } from './types';

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
    nearest: ItemData | null;
    nearestVersion: number;
}

export const useAppStore = create<AppState>(() => ({
    page: Page.home,
    tour: 'Tour',
    positionLatLng: null,
    loaders: [],
    nearest: null,
    nearestVersion: 0
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
        navigator.geolocation.watchPosition(async position => {
            console.log('position is', position);
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const oldPos = useAppStore.getState().positionLatLng;
            if (oldPos === null || lat !== oldPos[0] || lng !== oldPos[1]) {
                const newPos: LatLngTuple = [lat, lng];
                useAppStore.setState(state => ({ ...state, positionLatLng: newPos }));
                const request = idGenerator++;
                const best = await getNearest(lat, lng);
                console.log('nearest', best);
                // Only update the state if there hasn't been a more recent request
                useAppStore.setState(state =>
                    state.nearestVersion < request && state.nearest?.id !== best.id
                        ? { ...state, nearest: best, nearestVersion: request }
                        : state
                );
            }
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

export const getNearest = async (lat: number, lng: number): Promise<ItemData> => {
    // No need to show a loader during this operation
    const result = await fetch(`/nearest/${lat}/${lng}`, { credentials: 'include' });
    const json = (await result.json()) as ItemData;
    return json;
};

export const sendStory = async (siteId: string, story: string): Promise<void> => {
    // No need to show a loader during this operation
    await fetch(`/story/${siteId}`, {
        credentials: 'include',
        method: 'POST',
        body: story
    });
};

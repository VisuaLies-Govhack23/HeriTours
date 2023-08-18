import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import { initGeolocation } from './model';

const app = document.getElementById('app');
if (app) {
    createRoot(app).render(
        <React.StrictMode>
            <App />
        </React.StrictMode>
    );
    initGeolocation();
} else {
    console.error('Cannot start app.');
}

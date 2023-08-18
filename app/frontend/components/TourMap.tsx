import React from 'react';
import styled from '@emotion/styled';
import { primary } from 'frontend/constants';
import { LatLngTuple } from 'leaflet';
import { MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';

const ScreenColumn = styled.div`
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: stretch;
`;

const Title = styled.div`
    padding: 1rem;
`;

const position: LatLngTuple = [-33.885, 151.2];
const position1: LatLngTuple = [-33.9, 151.2];
const position2: LatLngTuple = [-33.87, 151.2];

export interface MapProps {}

const TourMap: React.FC<MapProps> = ({}) => {
    return (
        <ScreenColumn>
            <Title>Victorian Heritage</Title>
            <MapContainer
                style={{ flex: 1 }}
                center={position}
                zoom={13}
                scrollWheelZoom={true}
                attributionControl={false}>
                <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />
                <Polyline pathOptions={{ color: primary }} positions={[position1, position2]} />
                <Marker
                    position={position1}
                    eventHandlers={{
                        click() {
                            console.log('click');
                        }
                    }}>
                    <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
                <Marker
                    position={position2}
                    eventHandlers={{
                        click() {
                            console.log('click');
                        }
                    }}>
                    <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
            </MapContainer>
        </ScreenColumn>
    );
};

export default TourMap;

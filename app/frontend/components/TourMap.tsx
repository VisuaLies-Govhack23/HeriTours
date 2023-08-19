import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import { LatLngTuple } from 'leaflet';
import { MdClose } from 'react-icons/md';
import { CircleMarker, MapContainer, Marker, Polyline, TileLayer, Tooltip, useMap } from 'react-leaflet';
import { light, primary } from '../constants';
import { home, useAppStore } from '../model';
import Details from './Details';
import { Modal } from './Modal';
import Spinner from './Spinner';

const ScreenColumn = styled.div`
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: stretch;
`;

const TitleBlock = styled.div`
    display: flex;
    padding: 1rem;
    border-bottom: 6px solid ${primary};
`;

const CloseButton = styled.button`
    background: ${light};
    border: none;
    svg {
        width: 1rem;
        height: 1rem;
    }
`;

const Title = styled.div`
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
`;

const TooltipText = styled.div`
    font-family: 'Playfair Display';
`;

const position: LatLngTuple = [-33.885, 151.2];

const AutoZoom: React.FC<{ line: LatLngTuple[] }> = ({ line }) => {
    const map = useMap();
    useEffect(() => {
        setTimeout(() => {
            const lats = line.map(s => s[0]);
            const lngs = line.map(s => s[1]);
            const bounds = [
                [Math.min(...lats), Math.min(...lngs)] as LatLngTuple,
                [Math.max(...lats), Math.max(...lngs)] as LatLngTuple
            ];
            map.fitBounds(bounds, { maxZoom: 15, animate: true });
        }, 1000);
    }, []);
    return <></>;
};
export interface MapProps {}

const TourMap: React.FC<MapProps> = ({}) => {
    const [isShowingDetails, setShowingDetails] = useState(false);
    const tourName = useAppStore(state => state.tour);
    const route = useAppStore(state => state.route);
    const currentLocation = useAppStore(state => state.positionLatLng);

    const doClose = () => {
        setShowingDetails(false);
    };

    const doHome = () => {
        home();
    };

    const line = currentLocation
        ? [currentLocation, ...route.map(stop => stop.latlng)]
        : route.map(stop => stop.latlng);

    return (
        <>
            <ScreenColumn>
                <Spinner isDark={false} />
                <TitleBlock>
                    <Title>{tourName}</Title>
                    <CloseButton onClick={doHome}>
                        <MdClose />
                    </CloseButton>
                </TitleBlock>
                <MapContainer
                    style={{ flex: 1 }}
                    center={position}
                    zoom={13}
                    scrollWheelZoom={true}
                    attributionControl={false}>
                    <AutoZoom line={line} />
                    <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    {currentLocation && <CircleMarker center={currentLocation} />}
                    <Polyline pathOptions={{ color: primary }} positions={line} />
                    {route.map(stop => (
                        <Marker
                            position={stop.latlng}
                            eventHandlers={{
                                click() {
                                    console.log('click');
                                    setShowingDetails(true);
                                }
                            }}>
                            <Tooltip permanent={true}>
                                <TooltipText>{stop.name}</TooltipText>
                            </Tooltip>
                        </Marker>
                    ))}
                </MapContainer>
            </ScreenColumn>
            <Modal visible={isShowingDetails}>
                <Details onClose={doClose} />
            </Modal>
        </>
    );
};

export default TourMap;

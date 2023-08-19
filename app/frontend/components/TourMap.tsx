import React, { useState } from 'react';
import styled from '@emotion/styled';
import { LatLngTuple } from 'leaflet';
import { MdClose } from 'react-icons/md';
import { CircleMarker, MapContainer, Marker, Polyline, TileLayer, Tooltip } from 'react-leaflet';
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
`;

const TooltipText = styled.div`
    font-family: 'Playfair Display';
`;

const position: LatLngTuple = [-33.885, 151.2];
const position1: LatLngTuple = [-33.9, 151.2];
const position2: LatLngTuple = [-33.87, 151.2];

export interface MapProps {}

const TourMap: React.FC<MapProps> = ({}) => {
    const [isShowingDetails, setShowingDetails] = useState(false);
    const tourName = useAppStore(state => state.tour);
    const currentLocation = useAppStore(state => state.positionLatLng);

    const doClose = () => {
        setShowingDetails(false);
    };

    const doHome = () => {
        home();
    };

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
                    <TileLayer url="https://tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    {currentLocation && <CircleMarker center={currentLocation} />}
                    <Polyline pathOptions={{ color: primary }} positions={[position1, position2]} />
                    <Marker
                        position={position1}
                        eventHandlers={{
                            click() {
                                console.log('click');
                                setShowingDetails(true);
                            }
                        }}>
                        <Tooltip permanent={true}>
                            <TooltipText>Who was the first Governor?</TooltipText>
                        </Tooltip>
                    </Marker>
                    <Marker
                        position={position2}
                        eventHandlers={{
                            click() {
                                console.log('click');
                                setShowingDetails(true);
                            }
                        }}>
                        <Tooltip permanent={true}>
                            <TooltipText>What is Sydney's oldest boat?</TooltipText>
                        </Tooltip>
                    </Marker>
                </MapContainer>
            </ScreenColumn>
            <Modal visible={isShowingDetails}>
                <Details onClose={doClose} />
            </Modal>
        </>
    );
};

export default TourMap;

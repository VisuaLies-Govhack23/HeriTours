import React from 'react';
import styled from '@emotion/styled';
import { dark, light } from 'frontend/constants';

const OverlayContainer = styled.div`
    height: 100vh;
    width: 100vw;
    left: 0;
    top: 0;
    position: absolute;
    overflow-x: clip;
    overflow-y: clip;
    pointer-events: none;
`;

const Blur = styled.div<{ visible: boolean }>`
    height: 100vh;
    width: 100vw;
    left: 0;
    top: 0;
    position: absolute;
    background-color: ${dark};
    opacity: ${props => (props.visible ? '0.3' : '0')};
    transition: opacity 0.3s linear;
    z-index: 1000;
    overflow-x: clip;
    overflow-y: clip;
    pointer-events: ${props => (props.visible ? 'initial' : 'none')};
`;

const Overlay = styled.div<{ visible: boolean }>`
    height: calc(100vh - 2rem);
    width: calc(100vw - 2rem);
    top: ${props => (props.visible ? '1rem' : '100vh')};
    transition: top 0.3s ease-in-out;
    left: 1rem;
    position: absolute;
    background-color: ${light};
    z-index: 2000;
    pointer-events: initial;
`;

interface ModalProps {
    visible: boolean;
    children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({ visible, children }) => {
    return (
        <OverlayContainer>
            <Blur visible={visible} />
            <Overlay visible={visible}>{children}</Overlay>
        </OverlayContainer>
    );
};

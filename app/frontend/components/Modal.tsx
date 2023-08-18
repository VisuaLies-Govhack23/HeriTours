import React, { useState } from 'react';
import styled from '@emotion/styled';
import { dark, light } from 'frontend/constants';

// TODO finish this

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
    z-index: 1000;
    overflow-x: clip;
    overflow-y: clip;
    pointer-events: ${props => (props.visible ? 'initial' : 'none')};
`;

const Overlay = styled.div<{ visible: boolean }>`
    height: 100vh;
    width: 80vw;
    right: ${props => (props.visible ? '0rem' : '-80vw')};
    transition: right 0.3s ease-in-out;
    top: 0;
    position: absolute;
    background-color: ${light};
    z-index: 2000;
    pointer-events: initial;
`;

{
    /* <OverlayContainer>
<Blur visible={isShowingDetails} />
<Overlay visible={isShowingDetails}>Hello!</Overlay>
</OverlayContainer> */
}

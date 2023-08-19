import React from 'react';
import styled from '@emotion/styled';
import { light, primary } from '../constants';
import { useAppStore } from '../model';

const SpinnerBox = styled.div<{ isDark: boolean }>`
    overflow: hidden;
    height: 4px;
    position: relative;
    background-color: ${props => (props.isDark ? primary : light)};
    border: none;
`;

const SpinnerBlock = styled.div<{ isDark: boolean }>`
    width: 40vw;
    height: 4px;
    position: absolute;
    left: 0;
    background-color: ${props => (props.isDark ? light : primary)};
    top: 0;
    animation: spinner 2s linear infinite;
`;

export interface SpinnerProps {
    isDark: boolean;
}

const Spinner: React.FC<SpinnerProps> = ({ isDark }) => {
    const isLoading = useAppStore(state => state.loaders).length > 0;
    return <SpinnerBox isDark={isDark}>{isLoading && <SpinnerBlock isDark={isDark} />}</SpinnerBox>;
};

export default Spinner;

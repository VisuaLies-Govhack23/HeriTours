import React from 'react';
import styled from '@emotion/styled';
import { LuCompass } from 'react-icons/lu';
import { light, primary } from '../constants';

const LogoBox = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    padding: 0.5rem;
    background-color: ${primary};
    svg {
        color: ${light};
        padding-top: 0.25rem;
        height: 1.5rem;
        width: 1.5rem;
        margin-right: 0.5rem;
    }
`;

const Text = styled.div`
    color: ${light};
    font-size: 1.5rem;
    font-weight: 900;
`;

export interface LogoProps {}

const Logo: React.FC<LogoProps> = ({}) => {
    return (
        <LogoBox>
            <LuCompass />
            <Text>Visual Lives</Text>
        </LogoBox>
    );
};

export default Logo;

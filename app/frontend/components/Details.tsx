import React, { useState } from 'react';
import styled from '@emotion/styled';
import Citizen from './Citizen';

const ScreenColumn = styled.div`
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    z-index: 1000;
`;

const TabRow = styled.div`
    display: flex;
    flex-direction: row;
    align-items: stretch;
    padding: 0.5rem;
`;

const TabItem = styled.button`
    flex: 1;
    padding: 0.5rem;
    &:first-child {
        margin-right: 1rem;
    }
`;

const CloseButton = styled.button`
    padding: 0.5rem;
`;

const FormBody = styled.div`
    flex: 1;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
`;

const Header = styled.h4`
    font-weight: bold;
    font-size: 1rem;
    font-style: normal;
    padding: 0.5rem;
    margin: 1rem 0 0.5rem 0;
`;

const InfoBlock = styled.div`
    padding: 0.5rem;
`;

const Frame = styled.iframe`
    flex: 1;
    border: none;
`;

enum Tabs {
    about = 'about',
    insights = 'insights',
    citizen = 'citizen',
    checkin = 'checkin'
}

export interface DetailsProps {
    onClose(): void;
}

const Details: React.FC<DetailsProps> = ({ onClose }) => {
    const [tab, setTab] = useState(Tabs.about);

    let body: React.ReactNode;
    switch (tab) {
        case Tabs.about:
            body = (
                <FormBody>
                    <Header>Description</Header>
                    <InfoBlock>This building was created in 1895...</InfoBlock>
                    <Header>Construction Year</Header>
                    <InfoBlock>1895</InfoBlock>
                    <Header>Historical Significance</Header>
                    <InfoBlock>This building was created in 1895...</InfoBlock>
                </FormBody>
            );
            break;
        case Tabs.insights:
            body = <Frame src="/dashboard/demo" />;
            break;
        case Tabs.citizen:
            body = <Citizen />;
            break;
        case Tabs.checkin:
            body = <div>Check in</div>;
            break;
    }

    return (
        <ScreenColumn>
            <TabRow>
                <TabItem onClick={() => setTab(Tabs.about)}>About</TabItem>
                <TabItem onClick={() => setTab(Tabs.insights)}>Local Insights</TabItem>
                <TabItem onClick={() => setTab(Tabs.citizen)}>Your Stories</TabItem>
                <TabItem onClick={() => setTab(Tabs.checkin)}>Check In</TabItem>
                <CloseButton onClick={onClose}>Close</CloseButton>
            </TabRow>
            {body}
        </ScreenColumn>
    );
};

export default Details;

import React, { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import { useAutoAnimate } from '@formkit/auto-animate/react';
import { darkGrey, light, lightGrey, primary } from '../constants';
import { loadSite, sendAnswer, sendStory, sendVote } from '../model';
import { SiteInfoData, StoryData } from '../types';
import QuestionBox from './QuestionBox';
import Vote from './Vote';

const Column = styled.div`
    display: flex;
    flex-direction: column;
    align-items: stretch;
`;

const Header = styled.h4`
    font-weight: bold;
    font-size: 1rem;
    font-style: normal;
    padding: 0.5rem;
    margin: 1rem 0 0.5rem 0;
`;

const Textarea = styled.textarea`
    height: 5rem;
    margin: 0.5rem;
`;

const StoryBlock = styled.div`
    margin: 0.5rem;
    border-bottom: 1px solid ${lightGrey};
    padding-bottom: 0.5rem;
    &:last-child {
        border-bottom: none;
    }
`;

const StoryText = styled.div`
    white-space: pre-wrap;
`;

const InfoText = styled.div`
    padding: 0.5rem 0.5rem 2rem 0.5rem;
`;

const Row = styled.div`
    display: flex;
    justify-content: flex-end;
    padding: 0.5rem;
`;

const Button = styled.button`
    background-color: ${primary};
    border: none;
    border-radius: 0.5rem;
    padding: 1rem;
    min-width: 5rem;
    text-align: center;
    font-weight: 900;
    color: ${light};
    &:hover {
        background-color: ${darkGrey};
    }
`;

const Scrollable = styled.div`
    overflow-y: scroll;
    flex: 1;
`;

export interface StoryProps {
    story: StoryData;
}

const Story: React.FC<StoryProps> = ({ story }) => {
    return (
        <StoryBlock>
            <StoryText>{story.story}</StoryText>
        </StoryBlock>
    );
};
export interface CitizenProps {
    siteId: string;
}

const Citizen: React.FC<CitizenProps> = ({ siteId }) => {
    const [isListening, setListening] = useState(true);
    const [story, setStory] = useState('');
    const [parent] = useAutoAnimate();
    const [info, setInfo] = useState<SiteInfoData | null>(null);

    useEffect(() => {
        const action = async () => {
            const info = await loadSite(siteId);
            setInfo(info);
            console.log(info);
        };
        void action();
    }, []);

    const doSubmitStory = () => {
        if (info && story) {
            setListening(false);
            // Note: A story will currently be lost if there is a network error
            // TODO: add error handling
            void sendStory(siteId, story);
        }
    };

    const doVote = (vote: number) => {
        if (info) {
            void sendVote(siteId, vote);
            setInfo({ ...info, story: { ...info.story, vote } });
        }
    };

    const doAnswer = (questionId: string, answerId: string) => {
        if (info) {
            void sendAnswer(siteId, questionId, answerId);
        }
    };

    const storyCombined = story || (info?.story.story ?? '');

    if (info === null) {
        return <Header>Loading...</Header>;
    }

    return (
        <Scrollable ref={parent}>
            <Header>Your Vote</Header>
            <Vote value={info.story.vote ?? 0} onChange={doVote} />
            <Header>Help Us and Earn Points</Header>
            <QuestionBox questions={info.questions} answered={info.answered} onAnswer={doAnswer} />
            {isListening && (
                <Column>
                    <Header>Share Your Story</Header>
                    <Textarea
                        value={storyCombined}
                        onChange={e => setStory(e.target.value)}
                        placeholder="Tell your story about this item..."
                    />
                    <Row>
                        <Button onClick={doSubmitStory}>Share</Button>
                    </Row>
                </Column>
            )}
            <Header>Community Stories</Header>
            {info.stories.length === 0 && isListening && (
                <InfoText>Nobody has told their story yet. Start the conversation with your story!</InfoText>
            )}
            {!isListening && <InfoText>Thanks for sharing your story!</InfoText>}
            {info.stories.map((story, index) => (
                <Story key={index} story={story} />
            ))}
        </Scrollable>
    );
};

export default Citizen;
